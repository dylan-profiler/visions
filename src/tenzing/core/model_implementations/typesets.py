from tenzing.core.model_implementations.types import *
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
    - tenzing_datetime
    - tenzing_timedelta
    """

    def __init__(self):
        types = [
            tenzing_object,
            tenzing_bool + missing,
            tenzing_float + missing,
            tenzing_object + missing,
            tenzing_complex + missing,
            tenzing_categorical + missing,
            tenzing_datetime + missing,
            tenzing_timedelta + missing,
            tenzing_integer + missing + infinite,
            tenzing_string + missing,
        ]
        super().__init__(types)


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
    - tenzing_datetime
    - tenzing_timedelta
    - tenzing_geometry
    """

    def __init__(self):
        types = [
            tenzing_bool + missing,
            tenzing_float + missing,
            tenzing_object + missing,
            tenzing_complex + missing,
            tenzing_categorical + missing,
            tenzing_datetime + missing,
            tenzing_timedelta + missing,
            tenzing_integer + missing + infinite,
            tenzing_string + missing,
            tenzing_geometry + missing,
        ]
        super().__init__(types)


class tenzing_complete_set(tenzingTypeset):
    """Standard tenzing typeset with all supported types

    Includes support for the following types:
    - tenzing_float
    - tenzing_integer
    - tenzing_bool
    - tenzing_object
    - tenzing_string
    - tenzing_complex
    - tenzing_categorical
    - tenzing_datetime
    - tenzing_date
    - tenzing_time
    - tenzing_timedelta
    - tenzing_geometry
    - tenzing_path
    - tenzing_existing_path
    - tenzing_url
    """

    def __init__(self):
        types = [
            tenzing_bool + missing,
            tenzing_float + missing,
            tenzing_object + missing,
            tenzing_complex + missing,
            tenzing_categorical + missing,
            tenzing_datetime + missing,
            tenzing_timedelta + missing,
            tenzing_integer + missing + infinite,
            tenzing_string + missing,
            tenzing_geometry + missing,
            tenzing_url + missing,
            tenzing_path + missing,
            tenzing_date + missing,
            tenzing_time + missing,
            tenzing_existing_path + missing,
            tenzing_empty + missing,
        ]
        super().__init__(types)
