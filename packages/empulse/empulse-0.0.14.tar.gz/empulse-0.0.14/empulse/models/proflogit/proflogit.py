from functools import partial

import numpy as np
from sklearn.utils import check_array, check_X_y
from sklearn.base import BaseEstimator

from .common import NUM_TYPE
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
            soft_thd=True,
            rga_kws=None,
            score_function=empc_score,
            intercept=True,
            default_bounds=(-3, 3),
    ):
        # Check regularization parameters
        self.lambda_val = lambda_val
        self.alpha = alpha
        self.soft_thd = soft_thd

        # Check RGA parameters
        if rga_kws is None:
            rga_kws = {"niter": 1000, "niter_diff": 250}
        assert isinstance(rga_kws, dict), (
            "``rga_kws`` must be a dict, "
            "where keys are parameters. See help(proflogit.rga.RGA)."
        )
        self.rga_kws = rga_kws

        # Check intercept
        if not isinstance(intercept, bool):
            raise TypeError("`intercept` must be a boolean.")
        self.intercept = intercept

        # Check bounds
        assert isinstance(default_bounds, tuple) and len(default_bounds) == 2
        assert all(isinstance(v, NUM_TYPE) for v in default_bounds)
        self.default_bounds = default_bounds

        # Attributes
        self.n_dim = None
        self.rga = None
        self.score_function = score_function

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

        if "bounds" not in self.rga_kws:
            self.rga_kws["bounds"] = [self.default_bounds] * self.n_dim

        # Init
        score_function = partial(self.score_function, y_true=y)
        func_args = (
            X,
            {"lambda": self.lambda_val, "alpha": self.alpha, "soft-thd": self.soft_thd},
            score_function,
            self.intercept
        )
        self.rga = RGA(func=proflogit_fobj, args=func_args, **self.rga_kws)

        # Do optimization
        self.rga.solve()

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
        theta = self.rga.result.x
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


def proflogit_fobj(theta, *args):
    """ProfLogit's objective function (maximization problem)."""
    # Get function arguments
    X, reg_kws, score_function, intercept = args
    # X: (numpy.ndarray) standardized model matrix
    # reg_kws: (dict) regularization parameters
    # emp: (EMPChurn) object to compute EMPC
    # intercept: (bool) include intercept

    # Check theta
    # b refers to elements in theta; modifying b, will modify the corresponding
    # elements in theta
    # b is the vector holding the regression coefficients (no intercept)
    b = theta[1:] if intercept else theta

    def soft_thresholding_func(bvec, regkws):
        """Apply soft-thresholding."""
        bool_nonzero = (np.abs(bvec) - regkws["lambda"]) > 0
        if np.sum(bool_nonzero) > 0:
            bvec[bool_nonzero] = np.sign(bvec[bool_nonzero]) * (
                    np.abs(bvec[bool_nonzero]) - regkws["lambda"]
            )
        if np.sum(~bool_nonzero) > 0:
            bvec[~bool_nonzero] = 0
        return bvec

    def reg_term(bvec, regkws):
        """Elastic net regularization."""
        return 0.5 * (1 - regkws["alpha"]) * np.sum(bvec ** 2) + regkws[
            "alpha"
        ] * np.sum(np.abs(bvec))

    if reg_kws["soft-thd"]:
        b = soft_thresholding_func(b, reg_kws)
    logits = np.dot(X, theta)
    y_pred = 1 / (1 + np.exp(-logits))  # Invert logit transformation
    score = score_function(y_pred=y_pred)
    penalty = reg_kws["lambda"] * reg_term(b, reg_kws)
    fitness = score - penalty
    return fitness
