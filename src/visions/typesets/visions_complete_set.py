from visions.types import (
    visions_ip,
    visions_uuid,
    visions_image_path,
    visions_existing_path,
    visions_date,
    visions_time,
    visions_url,
    visions_path,
    visions_geometry,
    visions_string,
    visions_count,
    visions_integer,
    visions_timedelta,
    visions_datetime,
    visions_ordinal,
    visions_categorical,
    visions_complex,
    visions_object,
    visions_float,
    visions_bool,
)
from visions.typesets.typeset import VisionsTypeset


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
    - visions_uuid

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
            visions_uuid,
        }
        super().__init__(types)
