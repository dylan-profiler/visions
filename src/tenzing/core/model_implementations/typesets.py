from tenzing.core.typesets import tenzingTypeset
from tenzing.core.model_implementations import *

import pandas as pd


def _get_column_names(obj):
    if isinstance(obj, pd.DataFrame):
        return obj.columns.values.tolist()
    elif isinstance(obj, list):
        return obj


class tenzing_standard(tenzingTypeset):
    """The standard tenzing typesets

    Includes support for the following types:
    - tenzing_float
    - tenzing_integer
    - tenzing_bool
    - tenzing_object
    - tenzing_string
    - tenzing_complex
    - tenzing_categorical
    - tenzing_timestamp
    """
    def __init__(self):
        root_types = [tenzing_bool, tenzing_float, tenzing_object,
                      tenzing_complex, tenzing_categorical, tenzing_timestamp,
                      tenzing_integer]
        derivative_types = [tenzing_string]
        super().__init__(root_types, derivative_types)


class tenzing_geometry_set(tenzingTypeset):
    """Standard tenzing typeset with shapely geometry support

    Includes support for the following types:
    - tenzing_float
    - tenzing_integer
    - tenzing_bool
    - tenzing_object
    - tenzing_string
    - tenzing_complex
    - tenzing_categorical
    - tenzing_timestamp
    - tenzing_geometry
    """
    def __init__(self):
        root_types = [tenzing_bool, tenzing_float, tenzing_object,
                      tenzing_complex, tenzing_categorical, tenzing_timestamp,
                      tenzing_integer]
        derivative_types = [tenzing_string, tenzing_geometry]
        super().__init__(root_types, derivative_types)
