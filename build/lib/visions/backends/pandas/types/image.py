import imghdr
from pathlib import Path

import pandas as pd

from visions.backends.pandas.series_utils import series_handle_nulls, series_not_empty
from visions.types.image import Image


@Image.contains_op.register
@series_not_empty
@series_handle_nulls
def image_contains(series: pd.Series, state: dict) -> bool:
    return all(isinstance(p, Path) and p.exists() and imghdr.what(p) for p in series)
