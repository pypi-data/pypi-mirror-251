import numbers
from typing import overload

import numpy as np
from numpy.typing import ArrayLike

from ..validation import check_shape, check_positive, check_y_true, check_y_pred, check_gt_one, check_fraction


@overload
def _validate_input(
        y_true: ArrayLike,
        y_pred: ArrayLike,
        clv: ArrayLike,
        d: float,
        f: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ...


@overload
def _validate_input(
        y_true: ArrayLike,
        y_pred: ArrayLike,
        clv: float,
        d: float,
        f: float
) -> tuple[np.ndarray, np.ndarray, float]:
    ...


def _validate_input(
        y_true: ArrayLike,
        y_pred: ArrayLike,
        clv: float | ArrayLike,
        d: float,
        f: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray | float]:
    y_true = check_y_true(y_true)
    y_pred = check_y_pred(y_pred)
    check_shape(y_true, y_pred)
    if not isinstance(clv, numbers.Number):
        clv = np.asarray(clv)
        check_positive(float(np.mean(clv)), 'clv')
    else:
        check_positive(clv, 'clv')
    check_positive(d, 'incentive_cost')
    check_positive(f, 'contact_cost')
    if clv <= d:
        raise ValueError(f"clv should be greater than d, got a value of {clv} for clv and for {d} instead.")

    return y_true, y_pred, clv


def _validate_input_emp(
        y_true: ArrayLike,
        y_pred: ArrayLike,
        alpha: float,
        beta: float,
        clv: float | ArrayLike,
        d: float,
        f: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray | float]:
    check_gt_one(alpha, 'alpha')
    check_gt_one(beta, 'beta')
    return _validate_input(y_true, y_pred, clv, d, f)


def _validate_input_mp(
        y_true: ArrayLike,
        y_pred: ArrayLike,
        gamma: float,
        clv: float | ArrayLike,
        d: float,
        f: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray | float]:
    check_fraction(gamma, 'gamma')
    return _validate_input(y_true, y_pred, clv, d, f)
