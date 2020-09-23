"""Core functionality"""
try:
    import pandas as pd

    import visions.backends.pandas_functions

    if int(pd.__version__.split(".")[0]) < 1:
        from visions.dtypes.boolean import BoolDtype
except ImportError:
    pass

from visions import types, typesets, utils
from visions.functional import (
    cast_to_detected,
    cast_to_inferred,
    detect_type,
    infer_type,
)
from visions.types import *
from visions.typesets import *
