import numpy as np
from numpy.typing import ArrayLike

from ..validation import check_shape, check_positive, check_fraction, check_y_true, check_y_pred


def _validate_input(
        y_true: ArrayLike,
        y_pred: ArrayLike,
        contact_cost: float,
        sales_cost: float,
        direct_selling: float,
        commission: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Validate input for all acquisition parameters."""
    y_true = check_y_true(y_true)
    y_pred = check_y_pred(y_pred)
    check_shape(y_true, y_pred)
    check_positive(contact_cost, 'contact_cost')
    check_positive(sales_cost, 'sales_cost')
    check_fraction(direct_selling, 'direct_selling')
    check_fraction(commission, 'commission')

    return y_true, y_pred
