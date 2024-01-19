from functools import partial

import numpy as np
from sklearn.utils import check_array, check_X_y
from sklearn.base import BaseEstimator

from .rga import RGA
from empulse.metrics import empc_score


class ProfLogitClassifier(BaseEstimator):
    """
    ProfLogit for Customer Churn Prediction
    =======================================

    Maximizing empirical EMP for churn by optimizing
    the regression coefficients of the logistic model through
    a Real-coded Genetic Algorithm (RGA).

    Parameters
    ----------
    rga_kws : dict (default: None)
        Parameters passed to ``RGA``.
        If None, the following parameters are used:
        {
            'niter': 1000,
            'niter_diff': 250,
        }
        *Note*: When manually specifying ``rga_kws``, at least one of the
        following three parameters must be in the dict:
        ``niter``, ``niter_diff``, or ``nfev``.
        See help(proflogit.rga.RGA) for more information.

    intercept : bool (default: True)
        If True, intercept in the logistic model is taken into account.
        The corresponding all-ones vector should be in
        the first column of ``x``.

    default_bounds: tuple, default: (-3, 3)
        Bounds for every regression parameter. Use the ``bounds`` parameter
        through ``rga_kws`` for individual specifications.

    Attributes
    ----------
    rga : `proflogit.rga.RGA`
        RGA instance. The optimization result is stored under its ``res``
        attribute, which is represented as a `scipy.optimize.OptimizeResult`
        object with attributes:
          * ``x`` (ndarray) The solution of the optimization.
          * ``fun`` (float) Objective function value of the solution array.
          * ``success`` (bool) Whether the optimizer exited successfully.
          * ``message`` (str) Description of the cause of the termination.
          * ``nit`` (int) Number of iterations performed by the optimizer.
          * ``nit_diff`` (int) Number of consecutive non-improvements.
          * ``nfev`` (int) Number of evaluations of the objective functions.
        See `OptimizeResult` for a description of other attributes.

    References
    ----------
    [1] Stripling, E., vanden Broucke, S., Antonio, K., Baesens, B. and
        Snoeck, M. (2017). Profit Maximizing Logistic Model for
        Customer Churn Prediction Using Genetic Algorithms.
        Swarm and Evolutionary Computation.
    [2] Stripling, E., vanden Broucke, S., Antonio, K., Baesens, B. and
        Snoeck, M. (2015). Profit Maximizing Logistic Regression Modeling for
        Customer Churn Prediction. IEEE International Conference on
        Data Science and Advanced Analytics (DSAA) (pp. 1–10). Paris, France.

    """

    def __init__(
            self,
            lambda_val=0.1,
            alpha=1.0,
            soft_threshold=True,
            optimize_fn=None,
            score_function=empc_score,
            intercept=True,
            **kwargs,
    ):
        # Check regularization parameters
        self.lambda_val = lambda_val
        self.alpha = alpha
        self.soft_threshold = soft_threshold

        # Check intercept
        if not isinstance(intercept, bool):
            raise TypeError("`intercept` must be a boolean.")
        self.intercept = intercept

        # Attributes
        self.n_dim = None
        self.result = None
        self.score_function = score_function
        if optimize_fn is None:
            def optimize(objective):
                rga = RGA()
                while rga.result
            optimizer = RGA()
            self.optimize_fn = partial(RGA(**kwargs).optimize)
        self.optimize_fn = partial(optimize_fn, **kwargs)

    def fit(self, X, y):
        """
        Train ProfLogitCCP.

        Parameters
        ----------
        X : 2D numpy.ndarray, shape=(n_samples, n_dim)
            Standardized design matrix (zero mean and unit variance).

        y : 1D array-like or label indicator array, shape=(n_samples,)
            Binary target values. Churners have a ``case_label`` value.

        Returns
        -------
        self : object
            Returns self.

        """
        X, y = check_X_y(X, y)

        if self.intercept and not np.all(X[:, 0] == 1):
            X = np.hstack((np.ones((X.shape[0], 1)), X))
        self.n_dim = X.shape[1]

        if 'bounds' not in self.optimize_fn.keywords:
            self.optimize_fn = partial(self.optimize_fn, bounds=[(-3, 3)] * self.n_dim)

        objective = partial(
            proflogit_fobj,
            X=X,
            loss_fn=partial(self.score_function, y_true=y),
            lambda_val=self.lambda_val,
            alpha=self.alpha,
            soft_threshold=self.soft_threshold,
            intercept=self.intercept
        )
        self.result = self.optimize_fn(objective)

        return self

    def predict_proba(self, X):
        """
        Compute predicted probabilities.

        Parameters
        ----------
        X : 2D numpy.ndarray, shape=(n_samples, n_dim)
            Standardized design matrix (zero mean and unit variance).

        Returns
        -------
        y_score : 2D numpy.ndarray, shape=(n_samples, 2)
            Predicted probabilities.

        """
        X = check_array(X)
        if self.intercept and not np.all(X[:, 0] == 1):
            X = np.hstack((np.ones((X.shape[0], 1)), X))
        assert X.ndim == 2
        assert X.shape[1] == self.n_dim
        theta = self.result.x
        logits = np.dot(X, theta)
        y_score = 1 / (1 + np.exp(-logits))  # Invert logit transformation

        # create 2D array with complementary probabilities
        y_score = np.vstack((1 - y_score, y_score)).T
        return y_score

    def predict(self, X):
        """
        Compute predicted labels.

        Parameters
        ----------
        X : 2D numpy.ndarray, shape=(n_samples, n_dim)
            Standardized design matrix (zero mean and unit variance).

        Returns
        -------
        y_pred : 1D numpy.ndarray, shape=(n_samples,)
            Predicted labels.

        """
        y_score = self.predict_proba(X)
        y_pred = np.argmax(y_score, axis=1)
        return y_pred

    def score(self, X, y_true):
        """
        Compute performance score.

        Parameters
        ----------
        X : 2D numpy.ndarray, shape=(n_samples, n_dim)
            Standardized design matrix (zero mean and unit variance).

        y_true : 1D array-like or label indicator array, shape=(n_samples,)
            Binary target values. Churners have a ``case_label`` value.

        Returns
        -------
        score : float
            score

        """
        X, y_true = check_X_y(X, y_true)
        y_score = self.predict_proba(X)[:, 1]
        score = self.score_function(y_true, y_score)
        return score


def proflogit_fobj(theta, X, loss_fn, lambda_val, alpha, soft_threshold, intercept):
    """ProfLogit's objective function (maximization problem)."""

    # TODO: objective function alters values in theta which originate from the RGA, is this intended?
    # b refers to elements in theta; modifying b, will modify the corresponding elements in theta
    # b is the vector holding the regression coefficients (no intercept)
    b = theta[1:] if intercept else theta

    if soft_threshold:
        bool_nonzero = (np.abs(b) - lambda_val) > 0
        if np.sum(bool_nonzero) > 0:
            b[bool_nonzero] = np.sign(b[bool_nonzero]) * (
                    np.abs(b[bool_nonzero]) - lambda_val
            )
        if np.sum(~bool_nonzero) > 0:
            b[~bool_nonzero] = 0

    logits = np.dot(X, theta)
    y_pred = 1 / (1 + np.exp(-logits))  # Invert logit transformation
    loss = loss_fn(y_pred=y_pred)
    regularization_term = 0.5 * (1 - alpha) * np.sum(b ** 2) + alpha * np.sum(np.abs(b))
    penalty = lambda_val * regularization_term
    return loss - penalty


if __name__ == '__main__':
    from itertools import takewhile, islice
    from ..optimizers.optimizer import RGA

    def objective():
        ...



    def optimize(objective):
        optimizer = RGA()
        run_n_iterations = lambda data, n: islice(optimizer.optimize(data), n)
        run_until_convergence = lambda data, threshold: takewhile(
            lambda x: x.rel_improvement < threshold, optimizer.optimize(data)
        )

        run_n_iterations()

