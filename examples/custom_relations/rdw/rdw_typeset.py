from tenzing.core.model.types import tenzing_bool, tenzing_float, tenzing_object, tenzing_categorical, tenzing_ordinal, \
    tenzing_datetime, tenzing_timedelta, tenzing_integer, tenzing_string, tenzing_url, tenzing_date, tenzing_time
from tenzing.core.model.typeset import tenzingTypeset


class rdw_typeset(tenzingTypeset):
    """Typeset used in the RDW dataset"""

    def __init__(self):
        types = {
            tenzing_bool,
            tenzing_float,
            tenzing_object,
            tenzing_categorical,
            tenzing_ordinal,
            tenzing_datetime,
            tenzing_timedelta,
            tenzing_integer,
            tenzing_string,
            tenzing_url,
            tenzing_date,
            tenzing_time,
        }
        super().__init__(types)

        self.relations[tenzing_bool][tenzing_string].map.append({'Ja': True, 'Nee': False})

