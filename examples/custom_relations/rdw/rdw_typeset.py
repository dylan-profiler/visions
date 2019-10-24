from visions.core.implementations.types import (
    visions_bool,
    visions_float,
    visions_object,
    visions_categorical,
    visions_ordinal,
    visions_datetime,
    visions_timedelta,
    visions_integer,
    visions_string,
    visions_url,
    visions_date,
    visions_time,
    visions_complex,
)
from visions.core.model.typeset import VisionsTypeset
from visions.lib.relations.string_to_bool import string_to_bool_dutch
from visions.lib.relations.string_to_ordinal import string_to_ordinal


class rdw_typeset(VisionsTypeset):
    """Typeset used in the RDW dataset"""

    def __init__(self):
        types = {
            visions_bool,
            visions_float,
            visions_object,
            visions_categorical,
            visions_ordinal,
            visions_datetime,
            visions_timedelta,
            visions_integer,
            visions_string,
            visions_url,
            visions_date,
            visions_time,
            visions_complex,
        }
        super().__init__(types, build=False)

        self.relations[visions_ordinal][visions_string] = string_to_ordinal()
        self.relations[visions_bool][visions_string] = string_to_bool_dutch()
        self._build_graph()
