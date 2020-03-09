from visions.types import (
    visions_string,
    visions_integer,
    visions_timedelta,
    visions_datetime,
    visions_categorical,
    visions_complex,
    visions_float,
    visions_bool,
    visions_object,
)
from visions.typesets.typeset import VisionsTypeset


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
