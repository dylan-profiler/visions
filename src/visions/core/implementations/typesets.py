from visions.core.model.typeset import VisionsTypeset
from visions.core.implementations.types import *


class visions_standard_set(VisionsTypeset):
    """The standard visions typesets

    Includes support for the following types:

    - visions_float
    - visions_integer
    - visions_bool
    - visions_object
    - visions_string
    - visions_complex
    - visions_categorical
    - visions_datetime
    - visions_timedelta

    """

    def __init__(self):
        types = {
            visions_object,
            visions_bool,
            visions_float,
            visions_complex,
            visions_categorical,
            visions_datetime,
            visions_timedelta,
            visions_integer,
            visions_string,
        }
        super().__init__(types)


class visions_geometry_set(VisionsTypeset):
    """Standard visions typeset with shapely geometry support

    Includes support for the following types:

    - visions_float
    - visions_integer
    - visions_bool
    - visions_object
    - visions_string
    - visions_complex
    - visions_categorical
    - visions_datetime
    - visions_timedelta
    - visions_geometry

    """

    def __init__(self):
        types = {
            visions_bool,
            visions_float,
            visions_object,
            visions_complex,
            visions_categorical,
            visions_datetime,
            visions_timedelta,
            visions_integer,
            visions_string,
            visions_geometry,
        }
        super().__init__(types)


class visions_complete_set(VisionsTypeset):
    """Complete visions typeset with all supported types

    Includes support for the following types:

    - visions_float
    - visions_integer
    - visions_bool
    - visions_object
    - visions_string
    - visions_complex
    - visions_categorical
    - visions_ordinal
    - visions_count
    - visions_datetime
    - visions_date
    - visions_time
    - visions_timedelta
    - visions_geometry
    - visions_path
    - visions_existing_path
    - visions_image_path
    - visions_url
    - visions_ip

    """

    def __init__(self):
        types = {
            visions_bool,
            visions_float,
            visions_object,
            visions_complex,
            visions_categorical,
            visions_ordinal,
            visions_datetime,
            visions_timedelta,
            visions_integer,
            visions_count,
            visions_string,
            visions_geometry,
            visions_url,
            visions_path,
            visions_date,
            visions_time,
            visions_existing_path,
            visions_image_path,
            visions_ip,
        }
        super().__init__(types)
