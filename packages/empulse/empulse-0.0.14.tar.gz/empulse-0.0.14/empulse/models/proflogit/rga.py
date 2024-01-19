import datetime
import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import OptimizeResult
from .common import check_random_state
from .common import INTEGER_TYPES, FLOAT_TYPES


class RGA:
    """
    Real-coded Genetic Algorithm
    ============================

    Parameters
    ----------
    func : callable ``f(x, *args)``
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

    pop_size : None or int (default: None)
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

    disp : bool (default: False)
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
    res : OptimizeResult
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
            func,
            bounds,
            args=(),
            pop_size=None,
            crossover_rate=0.8,
            mutation_rate=0.1,
            elitism=0.05,
            niter=np.inf,
            niter_diff=np.inf,
            nfev=np.inf,
            disp=False,
            ftol=1e-4,
            random_state=None,
            n_jobs=1,
    ):
        self.name = "RGA"

        # Objective function to maximize
        self.func = func
        self.args = args

        # Check bounds
        bnd = list(bounds)
        assert all(
            isinstance(t, tuple)
            and len(t) == 2
            and isinstance(t[0], (INTEGER_TYPES, FLOAT_TYPES))
            and isinstance(t[1], (INTEGER_TYPES, FLOAT_TYPES))
            for t in bnd
        )
        ary_bnd = np.asarray(bnd, dtype=np.float64).T
        self.min_b = ary_bnd[0]
        self.max_b = ary_bnd[1]
        self.diff_b = np.fabs(self.max_b - self.min_b)
        self.n_dim = len(bnd)

        # Check population size
        if pop_size is None:
            self.pop_size = self.n_dim * 10
        else:
            assert isinstance(pop_size, INTEGER_TYPES) and pop_size >= 10
            self.pop_size = pop_size

        # Check crossover rate
        assert 0.0 <= crossover_rate <= 1.0
        self.crossover_rate = crossover_rate

        # Check mutation rate
        assert 0.0 <= mutation_rate <= 1.0
        self.mutation_rate = mutation_rate

        # Check elitism parameter
        assert isinstance(elitism, (INTEGER_TYPES, FLOAT_TYPES))
        if isinstance(elitism, INTEGER_TYPES):
            assert 0 <= elitism <= self.pop_size
            self.elitism = int(elitism)
        else:
            assert 0.0 <= elitism <= 1.0
            self.elitism = int(max(1, round(self.pop_size * elitism)))

        # Check niter, niter_diff, and nfev
        assert (
                np.isfinite(niter) or np.isfinite(niter_diff) or np.isfinite(nfev)
        )
        if np.isfinite(niter):
            assert isinstance(niter, INTEGER_TYPES) and niter > 0
        self.niter = niter

        if np.isfinite(niter_diff):
            assert isinstance(niter_diff, INTEGER_TYPES) and niter_diff > 0
        self.niter_diff = niter_diff

        if np.isfinite(nfev):
            assert isinstance(nfev, INTEGER_TYPES) and nfev > 0
        self.nfev = nfev

        # Check disp
        assert isinstance(disp, bool)
        self.disp = disp

        # Check ftol
        assert isinstance(ftol, FLOAT_TYPES) and ftol >= 0.0
        self.ftol = ftol

        # Get random state object
        self.rng = check_random_state(random_state)

        self.n_jobs = n_jobs

        # Attributes
        self._nit_diff = 0
        self._nit = 0
        self._nfev = 0
        self._n_mating_pairs = int(self.pop_size / 2)  # Constant for crossover
        self.population = None
        self.elite_pool = None
        self.fitness = np.empty(self.pop_size) * np.nan
        self.fx_best = []
        self.res = OptimizeResult(success=False)

    def init(self):
        rnd_pop = self.rng.rand(self.pop_size, self.n_dim)
        return self.min_b + rnd_pop * self.diff_b

    def evaluate(self) -> bool:
        fitness_values = Parallel(n_jobs=self.n_jobs)(delayed(self.update_fitness)(ix) for ix in range(self.pop_size))
        self.fitness = np.asarray(fitness_values)
        return False

    def update_fitness(self, index: int) -> float:
        fitness_value = float(self.fitness[index])
        if np.isnan(fitness_value):
            return self.func(self.population[index], *self.args)
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
            relative_fitness = np.ones(self.pop_size) / self.pop_size  # Uniform distribution
        else:
            relative_fitness = scaled_fitness / normalization_factor
        select_ix = self.rng.choice(
            self.pop_size, size=self.pop_size, replace=True, p=relative_fitness,
        )
        self.population = self.population[select_ix]
        self.fitness = self.fitness[select_ix]

    def crossover(self):
        """Perform local arithmetic crossover"""
        # Make iterator for pairs
        match_parents = (
            rnd_pair for rnd_pair in self.rng.choice(self.pop_size, (self._n_mating_pairs, 2), replace=False)
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
        for ix in range(self.pop_size):
            if self.rng.uniform() < self.mutation_rate:
                mutant = self.population[ix]  # inplace
                rnd_gene = self.rng.choice(self.n_dim)
                rnd_val = self.rng.uniform(
                    low=self.min_b[rnd_gene], high=self.max_b[rnd_gene],
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

    def update(self):
        """
        Update population by replacing the worst solutions of the current
        with the ones from the elite pool.
        Then, update the elite pool.
        Also, check if there has been an improvement in
        the best-so-far solution.
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
        self.update_elite_pool()
        is_fdiff = self.fx_best[-1] > (self.fx_best[-2] + self.ftol)
        if is_fdiff:
            self._nit_diff = 0
        else:
            self._nit_diff += 1

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

    def _print_status_message(self):
        status_msg = "Iter = {:5d}; nfev = {:6d}; fx = {:.4f}".format(
            self._nit, self._nfev, self.fx_best[-1],
        )
        print(status_msg)

    def solve(self):
        self.population = self.init()
        init_break = self.evaluate()
        self.update_elite_pool()

        if init_break:
            run_main_loop = False
            self.res.message = (
                "Maximum number of function evaluations has been reached "
                "during initialization."
            )
        else:
            run_main_loop = True

        # Do the optimization
        if self.disp:
            print(
                "# ---  {} ({})  --- #".format(
                    self.name,
                    datetime.datetime.now().strftime("%a %b %d %H:%M:%S"),
                )
            )

        while run_main_loop:
            if self.disp:
                self._print_status_message()
            self.select()  # parent selection
            self.crossover()
            self.mutate()
            break_loop = self.evaluate()
            self.update()  # survivor selection: overlapping-generation model
            self._nit += 1
            if break_loop:
                self.res.message = (
                    "Maximum number of function evaluations has been reached."
                )
                break
            if self._nit >= self.niter:
                self.res.message = (
                    "Maximum number of iterations has been reached."
                )
                break
            if self._nit_diff >= self.niter_diff:
                self.res.message = (
                    "Maximum number of consecutive non-improvements has been "
                    "reached."
                )
                break

        stop_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S")

        if any(np.isnan(fx) for fx in self.fitness):
            sorted_fx = self._get_sorted_non_nan_ix()
            best_ix = [t[0] for t in sorted_fx][-1]
        else:
            best_ix = np.argmax(self.fitness)
        self.res.x = np.copy(self.population[best_ix])
        self.res.fun = self.fitness[best_ix]
        self.res.success = True
        self.res.nit = self._nit
        self.res.nit_diff = self._nit_diff
        self.res.nfev = self._nfev
        if self.disp:
            self._print_status_message()
            print(self.res)
            print("# ---  {} ({})  --- #".format(self.name, stop_time))
