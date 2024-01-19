import numpy as np
from scipy.spatial import ConvexHull, QhullError

from sklearn.metrics import roc_curve


# def roc_curve(y_true: np.ndarray, y_pred: np.ndarray, pos_label=1, drop_intermediate: bool = True):
#     y_true = y_true == pos_label
#
#     # sort scores and corresponding truth values
#     desc_score_indices = np.argsort(y_pred)[::-1]
#     y_score = y_pred[desc_score_indices]
#     y_true_d = y_true[desc_score_indices]
#
#     # y_score typically has many tied values. Here we extract
#     # the indices associated with the distinct values. We also
#     # concatenate a value for the end of the curve.
#     distinct_value_indices = np.nonzero(np.diff(y_score))[0]
#     threshold_idxs = np.r_[distinct_value_indices, y_true_d.size - 1]
#
#     # accumulate the true positives with decreasing threshold
#     tps = np.cumsum(y_true)[threshold_idxs]
#     fps = 1 + threshold_idxs - tps
#
#     # Attempt to drop thresholds corresponding to points in between and
#     # collinear with other points. These are always suboptimal and do not
#     # appear on a plotted ROC curve (and thus do not affect the AUC).
#     # Here np.diff(_, 2) is used as a "second derivative" to tell if there
#     # is a corner at the point. Both fps and tps must be tested to handle
#     # thresholds with multiple data points (which are combined in
#     # _binary_clf_curve). This keeps all cases where the point should be kept,
#     # but does not drop more complicated cases like fps = [1, 3, 7],
#     # tps = [1, 2, 4]; there is no harm in keeping too many thresholds.
#     if drop_intermediate and len(fps) > 2:
#         optimal_idxs = np.where(
#             np.r_[True, np.logical_or(np.diff(fps, 2), np.diff(tps, 2)), True]
#         )[0]
#         fps = fps[optimal_idxs]
#         tps = tps[optimal_idxs]
#
#     # Add an extra threshold position
#     # to make sure that the curve starts at (0, 0)
#     tps = np.r_[0, tps]
#     fps = np.r_[0, fps]
#
#     if fps[-1] <= 0:
#         # warnings.warn(
#         #     "No negative samples in y_true, false positive value should be meaningless",
#         #     UndefinedMetricWarning,
#         # )
#         fpr = np.repeat(np.nan, fps.shape)
#     else:
#         fpr = fps / fps[-1]
#
#     if tps[-1] <= 0:
#         # warnings.warn(
#         #     "No positive samples in y_true, true positive value should be meaningless",
#         #     UndefinedMetricWarning,
#         # )
#         tpr = np.repeat(np.nan, tps.shape)
#     else:
#         tpr = tps / tps[-1]
#
#     return fpr, tpr


def compute_convex_hull(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        expand_dims: bool = False
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the convex hull points of the ROC curve.

    Parameters
    ----------
    y_true : 1D np.ndarray, shape=(n_samples,)
        Binary target values.

    y_pred : 1D np.ndarray, shape=(n_samples,)
        Target scores, can either be probability estimates or non-thresholded decision values.

    expand_dims : bool, default=False
        Whether to expand the dimensions of the convex hull points to (n_points, 1).

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Convex Hull points of the ROC curve (TPR, FPR)
    """
    # tpr, fpr = roc_curve(y_true, y_pred, drop_intermediate=True,)
    fpr, tpr, _ = roc_curve(y_true, y_pred, pos_label=1, drop_intermediate=True)
    # fpr, tpr = roc_curve(y_true, y_pred, pos_label=1, drop_intermediate=True)
    if fpr[0] != 0 or tpr[0] != 0:
        fpr = np.concatenate([[0], fpr])
        tpr = np.concatenate([[0], tpr])
    if fpr[-1] != 1 or tpr[-1] != 1:
        fpr = np.concatenate([fpr, [1]])
        tpr = np.concatenate([tpr, [1]])

    is_finite = np.isfinite(fpr) & np.isfinite(tpr)
    fpr = fpr[is_finite]
    tpr = tpr[is_finite]
    if fpr.shape[0] < 2:
        raise ValueError("Too few distinct predictions for ROCCH")

    points = np.c_[fpr, tpr]  # concatenate into matrix with two columns
    try:
        ind = ConvexHull(points).vertices  # indices of the points on the convex hull
    except QhullError:
        return np.array([0, 1]), np.array([0, 1])

    convex_hull_fpr = fpr[ind]
    convex_hull_tpr = tpr[ind]
    ind_upper_triangle = convex_hull_fpr < convex_hull_tpr  # only consider points above the 45° line
    convex_hull_fpr = np.concatenate([[0], convex_hull_fpr[ind_upper_triangle], [1]])
    convex_hull_tpr = np.concatenate([[0], convex_hull_tpr[ind_upper_triangle], [1]])
    ind = np.argsort(convex_hull_fpr)  # sort along the x-axis
    convex_hull_fpr = convex_hull_fpr[ind]
    convex_hull_tpr = convex_hull_tpr[ind]

    if expand_dims:
        convex_hull_tpr = np.expand_dims(convex_hull_tpr, axis=1)
        convex_hull_fpr = np.expand_dims(convex_hull_fpr, axis=1)

    return convex_hull_tpr, convex_hull_fpr
