"""Core functionality"""

from visions import test, types, typesets, utils
from visions.backends import *
from visions.declarative import create_type
from visions.functional import (
    cast_to_detected,
    cast_to_inferred,
    detect_type,
    infer_type,
)
from visions.types import *
from visions.typesets import *

__version__ = "0.8.1"
