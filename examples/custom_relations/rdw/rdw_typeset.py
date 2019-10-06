from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.types import (
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
    tenzing_complex)
from tenzing.core.model.typeset import tenzingTypeset
from tenzing.lib.relations.string_to_bool import string_to_bool_dutch
from tenzing.lib.relations.string_to_ordinal import string_to_ordinal


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
            tenzing_complex,
        }
        super().__init__(types, build=False)

        self.relations[tenzing_ordinal][tenzing_string] = string_to_ordinal()
        self.relations[tenzing_bool][tenzing_string] = string_to_bool_dutch()
        self._build_graph()
