from visions.types import (
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
)
from visions.typesets.typeset import VisionsTypeset


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
