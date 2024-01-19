import datetime
from functools import partial
from typing import Callable, Generator, Self

import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import OptimizeResult
from .common import check_random_state


class RGA:
    """
    Real-coded Genetic Algorithm
    ============================

    Parameters
    ----------
    objective : callable ``f(x, *args)``
        The objective function to be maximized.  Must be in the form
        ``f(x, *args)``, where ``x`` is the argument in the form of a 1-D array
        and ``args`` is a tuple of any additional fixed parameters needed to
        completely specify the function.

    bounds : sequence
        Bounds for variables.  ``(min, max)`` pairs for each element in ``x``,
        defining the lower and upper bounds for the optimizing argument of
        `func`. It is required to have ``len(bounds) == len(x)``.
        ``len(bounds)`` is used to determine the number of parameters in ``x``.
        For example, for a 2D problem with -10 <= x_i <= 10, i=1,2, specify:
        ``bounds=[(-10, 10)] * 2``.

    args : tuple, optional
        Any additional fixed parameters needed to
        completely specify the objective function.

    population_size : None or int (default: None)
        If None, ``popsize`` is 10 * number of parameters.
        If int, ``popsize`` must be a positive integer >= 10.

    crossover_rate : float (default: 0.8)
        Perform local arithmetic crossover with probability ``crossover_rate``.

    mutation_rate : float (default: 0.1)
        Perform uniform random mutation with probability ``mutation_rate``.

    elitism : int or float (default: 0.05)
        Number of the fittest chromosomes to survive to the next generation.
        If float, ``elitism`` is ``int(max(1, round(popsize * elitism)))``.
        If int and larger than ``popsize``, an exception is raised.

    niter : int (default: np.inf)
        The maximum number of generations over which the entire population is
        evolved.
        If np.inf, ``nfev`` or ``niter_diff`` must be specified.
        If int, it must be larger than zero. In this case, the algorithm stops
        when ``niter`` is reached, or possibly earlier when ``niter_diff``
        or ``nfev`` are specified as well.

    niter_diff : int (default: np.inf)
        Stop the algorithm if the fitness (with ``ftol`` tolerance)
        between consecutive best-so-far solutions remains the same for
        ``niter_diff`` number of iterations.
        If np.inf, ``niter`` or ``nfev`` must be specified.
        If int, it must be larger than zero. In this case, the algorithm stops
        when ``niter_diff`` is reached, or possibly earlier when ``niter``
        or ``nfev`` are specified as well.

    nfev : int (default: np.inf)
        The maximum number of function evaluations over which the population is
        evolved.
        If np.inf, ``niter`` or ``niter_diff`` must be specified.
        If int, it must be larger than zero. In this case, the algorithm stops
        when ``nfev`` is reached, or possibly earlier when ``niter_diff`` or
        ``niter`` are specified as well.

    verbose : bool (default: False)
        Set to True to print status messages.

    ftol : float (default: 1e-4)
        Absolute tolerance for convergence. See ``niter_diff``.

    random_state : None or int or `np.random.RandomState` (default: None)
        If None, a new `np.random.RandomState` is used;
        If int, a new `np.random.RandomState` with ``random_state`` as
        seed is used;
        If ``random_state`` is already a `np.random.RandomState` instance,
        that instance is used.

    Attributes
    ----------
    result : OptimizeResult
        The optimization result represented as a
        `scipy.optimize.OptimizeResult` object.
        Important attributes are:
          * ``x`` (ndarray) The solution of the optimization.
          * ``fun`` (float) Objective function value of the solution array.
          * ``success`` (bool) Whether the optimizer exited successfully.
          * ``message`` (str) Description of the cause of the termination.
          * ``nit`` (int) Number of iterations performed by the optimizer.
          * ``nit_diff`` (int) Number of consecutive non-improvements.
          * ``nfev`` (int) Number of evaluations of the objective functions.
        See `OptimizeResult` for a description of other attributes.

    fx_best : list
        Fitness values of the best solution per generation,
        including the zero generation (initialization).

    """

    def __init__(
            self,
            population_size=None,
            crossover_rate=0.8,
            mutation_rate=0.1,
            elitism=0.05,
            verbose=False,
            logging_fn=print,
            random_state=None,
            n_jobs=1,
    ):
        self.name = "RGA"

        if population_size is not None:
            if not isinstance(population_size, int):
                raise TypeError("`pop_size` must be an int.")
            if population_size < 10:
                raise ValueError("`pop_size` must be >= 10.")
        self.population_size = population_size

        if not 0.0 <= crossover_rate <= 1.0:
            raise ValueError("`crossover_rate` must be in [0, 1].")
        self.crossover_rate = crossover_rate

        if not 0.0 <= mutation_rate <= 1.0:
            raise ValueError("`mutation_rate` must be in [0, 1].")
        self.mutation_rate = mutation_rate

        if isinstance(elitism, int):
            if not 0 <= elitism <= self.population_size:
                raise ValueError("if `elitism` is an int, then `elitism` must be in [0, pop_size].")
            self.elitism = elitism
        elif isinstance(elitism, float):
            if not 0.0 <= elitism <= 1.0:
                raise ValueError("if `elitism` is a float, then `elitism` must be in [0, 1].")
            self.elitism = int(max(1, round(self.population_size * elitism)))
        else:
            raise TypeError("`elitism` must be an int or float.")

        self.verbose = verbose
        self.logging_fn = logging_fn

        # Get random state object
        self.rng = check_random_state(random_state)

        self.n_jobs = n_jobs

        # Attributes
        self._n_mating_pairs = int(self.population_size / 2)  # Constant for crossover
        self.population = None
        self.elite_pool = None
        self.fitness = np.empty(self.population_size) * np.nan
        self.fx_best = []
        self.result = OptimizeResult(success=False)

    def optimize(self, objective: Callable, bounds: tuple, args: tuple) -> Generator[Self, None, None]:
        objective = partial(objective, *args)
        # Check bounds
        bounds = list(bounds)
        if not all(
            isinstance(t, tuple)
            and len(t) == 2
            and isinstance(t[0], (int, float))
            and isinstance(t[1], (int, float))
            for t in bounds
        ):
            raise ValueError("`bounds` must be a sequence of tuples of two numbers (lower_bound, upper_bound).")
        ary_bnd = np.asarray(bounds, dtype=np.float64).T
        self.lower_bounds = ary_bnd[0]
        self.upper_bounds = ary_bnd[1]
        self.delta_bounds = np.fabs(self.upper_bounds - self.lower_bounds)
        self.n_dim = len(bounds)

        # Check population size
        if self.population_size is None:
            self.population_size = self.n_dim * 10

        self.population = self.generate_population()
        self.evaluate(objective)
        self.update_elite_pool()

        if self.verbose:
            self._log_start()

        while True:
            yield self
            if self.verbose:
                self._log_progress()
            self.select()
            self.crossover()
            self.mutate()
            self.evaluate(objective)
            self.insert_elites()  # survivor selection: overlapping-generation model
            self.update_elite_pool()

    def generate_population(self):
        population = self.rng.rand(self.population_size, self.n_dim)
        return self.lower_bounds + population * self.delta_bounds

    def evaluate(self, objective) -> bool:
        fitness_values = Parallel(n_jobs=self.n_jobs)(
            delayed(self.update_fitness)(ix, objective) for ix in range(self.population_size)
        )
        self.fitness = np.asarray(fitness_values)
        return False

    def update_fitness(self, objective, index: int) -> float:
        fitness_value = float(self.fitness[index])
        if np.isnan(fitness_value):
            return objective(self.population[index])
        else:
            return fitness_value

    def select(self):
        """Perform linear scaling selection"""
        fitness_values = np.copy(self.fitness)
        min_fitness = np.min(fitness_values)
        avg_fitness = np.mean(fitness_values)
        max_fitness = np.max(fitness_values)
        if min_fitness < 0:
            fitness_values -= min_fitness
            min_fitness = 0
        if min_fitness > (2 * avg_fitness - max_fitness):
            denominator = max_fitness - avg_fitness
            a = avg_fitness / (denominator if denominator != 0 else 1e-10)
            b = a * (max_fitness - 2 * avg_fitness)
        else:
            denominator = avg_fitness - min_fitness
            a = avg_fitness / (denominator if denominator != 0 else 1e-10)
            b = -min_fitness * a
        scaled_fitness = np.abs(a * fitness_values + b)
        if (normalization_factor := np.sum(scaled_fitness)) == 0:
            relative_fitness = np.ones(self.population_size) / self.population_size  # Uniform distribution
        else:
            relative_fitness = scaled_fitness / normalization_factor
        select_ix = self.rng.choice(
            self.population_size, size=self.population_size, replace=True, p=relative_fitness,
        )
        self.population = self.population[select_ix]
        self.fitness = self.fitness[select_ix]

    def crossover(self):
        """Perform local arithmetic crossover"""
        # Make iterator for pairs
        match_parents = (
            rnd_pair for rnd_pair in self.rng.choice(self.population_size, (self._n_mating_pairs, 2), replace=False)
        )

        # Crossover parents
        for ix1, ix2 in match_parents:
            if self.rng.uniform() < self.crossover_rate:
                parent1 = self.population[ix1]  # Pass-by-ref
                parent2 = self.population[ix2]
                w = self.rng.uniform(size=self.n_dim)
                child1 = w * parent1 + (1 - w) * parent2
                child2 = w * parent2 + (1 - w) * parent1
                self.population[ix1] = child1
                self.population[ix2] = child2
                self.fitness[ix1] = np.nan
                self.fitness[ix2] = np.nan

    def mutate(self):
        """Perform uniform random mutation"""
        for ix in range(self.population_size):
            if self.rng.uniform() < self.mutation_rate:
                mutant = self.population[ix]  # inplace
                rnd_gene = self.rng.choice(self.n_dim)
                rnd_val = self.rng.uniform(
                    low=self.lower_bounds[rnd_gene], high=self.upper_bounds[rnd_gene],
                )
                mutant[rnd_gene] = rnd_val
                self.fitness[ix] = np.nan

    def _get_sorted_non_nan_ix(self):
        """Get indices sorted according to non-nan fitness values"""
        non_nan_fx = (
            (ix, fx) for ix, fx in enumerate(self.fitness) if ~np.isnan(fx)
        )
        sorted_list = sorted(non_nan_fx, key=lambda t: t[1])
        return sorted_list

    def insert_elites(self):
        """
        Update population by replacing the worst solutions of the current
        with the ones from the elite pool.
        """
        if any(np.isnan(fx) for fx in self.fitness):
            sorted_fx = self._get_sorted_non_nan_ix()
            worst_ix = [t[0] for t in sorted_fx][: self.elitism]
        else:
            worst_ix = np.argsort(self.fitness)[: self.elitism]  # TODO: replace with argpartition
        for i, ix in enumerate(worst_ix):
            elite, fitness_elite = self.elite_pool[i]
            self.population[ix] = elite
            self.fitness[ix] = fitness_elite

    def update_elite_pool(self):
        if any(np.isnan(fx) for fx in self.fitness):
            sorted_fx = self._get_sorted_non_nan_ix()
            elite_ix = [t[0] for t in sorted_fx][-self.elitism:]
        else:
            elite_ix = np.argsort(self.fitness)[-self.elitism:]  # TODO: replace with argpartition
        self.elite_pool = [
            (self.population[ix].copy(), self.fitness[ix]) for ix in elite_ix
        ]
        # Append best solution
        self.fx_best.append(self.fitness[elite_ix[-1]])

    def _log_start(self):
        self.logging_fn(
            "# ---  {} ({})  --- #".format(
                self.name,
                datetime.datetime.now().strftime("%a %b %d %H:%M:%S"),
            )
        )

    def _log_progress(self):
        status_msg = "Iter = {:5d}; nfev = {:6d}; fx = {:.4f}".format(
            self._nit, self._nfev, self.fx_best[-1],
        )
        self.logging_fn(status_msg)

    def _log_end(self, stop_time):
        self.logging_fn(self.result)
        self.logging_fn("# ---  {} ({})  --- #".format(self.name, stop_time))


def run_n_iterations(objective, n) -> OptimizeResult:
    optimizer = RGA()
    run_n_iterations = lambda data, n: islice(optimizer.optimize(data), n)
    return OptimizeResult(
        ...
    )

def run_until_convergence(objective):
    optimizer = RGA()
    run_until_convergence = lambda data, threshold: takewhile(
        lambda x: x.rel_improvement < threshold, optimizer.optimize(data)
    )