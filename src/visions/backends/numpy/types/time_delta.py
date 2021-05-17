import numpy as np

from visions.backends.numpy.array_utils import array_not_empty
from visions.types.time_delta import TimeDelta


@TimeDelta.contains_op.register
@array_not_empty
def time_delta_contains(array: np.ndarray, state: dict) -> bool:
    """
    Example:
        >>> x = pd.array([pd.Timedelta(days=i) for i in range(3)])
        >>> x in visions.Timedelta
        True
    """
    return np.issubdtype(array.dtype, np.timedelta64)
