"""Core functionality"""
import pandas as pd

from visions import types, typesets, utils

if pd.__version__.split(".")[0] == 0:
    from visions.dtypes.boolean import BoolDtype

from visions.functional import (
    cast_frame,
    cast_series,
    detect_frame_type,
    detect_series_type,
    infer_frame_type,
    infer_series_type,
)
from visions.types import *
from visions.typesets import *
