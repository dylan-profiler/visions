from visions import visions_bool
from visions.core.implementations import visions_complete_set

# make Dutch boolean
from visions.lib.relations.string_to_bool import get_language_bool
from visions.lib.relations.string_to_categorical import (
    string_to_categorical_distinct_count,
)

visions_bool_nl = get_language_bool("nl")

# recognizes YYYYMMDD
from visions.core.implementations.types.visions_integer import (
    _get_relations,
    visions_integer,
)
from visions.lib.relations.integer_to_datetime import integer_to_datetime_year_month_day


@classmethod
def compose_relations_int(cls):
    return _get_relations(cls) + [integer_to_datetime_year_month_day(cls)]


visions_integer_ddt = visions_integer.extend_relations(
    "with_datetime", compose_relations_int
)

# string to category
from visions.core.implementations.types.visions_categorical import (
    _get_relations as cat_rel,
    visions_categorical,
)

# TODO: ensure that string_to_categorical is evaluated last (catch all)
@classmethod
def compose_relations_cat(cls):
    return cat_rel(cls) + [string_to_categorical_distinct_count(cls)]


visions_categorical_str = visions_categorical.extend_relations(
    "str", compose_relations_cat
)

rdw_typeset = visions_complete_set()
rdw_typeset -= visions_bool
rdw_typeset += visions_bool_nl
rdw_typeset -= visions_integer
rdw_typeset += visions_integer_ddt
rdw_typeset -= visions_categorical
rdw_typeset += visions_categorical_str
