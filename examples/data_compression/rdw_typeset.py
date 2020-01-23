import pandas as pd

from visions import visions_bool, visions_ordinal
from visions.core.implementations import visions_complete_set

# make Dutch boolean
from visions.lib.relations.categorical_to_ordinal import categorical_to_ordinal
from visions.lib.relations.string_to_bool import get_language_bool
from visions.lib.relations.string_to_categorical import (
    string_to_categorical_distinct_count,
)
from visions.core.implementations.types.visions_integer import (
    _get_relations as _get_relations_integer,
)
from visions.core.implementations.types.visions_ordinal import (
    _get_relations as _get_relations_ordinal,
)

from visions.core.implementations.types.visions_integer import visions_integer
from visions.lib.relations.integer_to_datetime import integer_to_datetime_year_month_day
from visions.core.implementations.types.visions_categorical import (
    _get_relations as _get_relations_categorical,
    visions_categorical,
)


# TODO: mutable
# type.update() -> new type
# typeset.update
#   => traverse graph; update (recursively) all InferentialRelations pointing to me

# TODO: add one relation


visions_bool_nl = get_language_bool("nl")


@classmethod
def compose_relations_int(cls):
    relations = _get_relations_integer(cls)
    return relations + [integer_to_datetime_year_month_day(cls)]


visions_integer_ddt = visions_integer.extend_relations(
    "with_datetime", compose_relations_int
)


@classmethod
def compose_relations_ordinal(cls):
    relations = _get_relations_ordinal(cls)
    return relations + [categorical_to_ordinal(cls)]


visions_ordinal_az = visions_ordinal.extend_relations(
    "with_az", compose_relations_ordinal
)

# string to category

# TODO: ensure that string_to_categorical is evaluated last (catch all)
@classmethod
def compose_relations_cat(cls):
    return _get_relations_categorical(cls) + [string_to_categorical_distinct_count(cls)]


visions_categorical_str = visions_categorical.extend_relations(
    "str", compose_relations_cat
)

rdw_typeset = visions_complete_set()
rdw_typeset = rdw_typeset.replace(visions_bool, visions_bool_nl)
rdw_typeset = rdw_typeset.replace(visions_integer, visions_integer_ddt)
rdw_typeset = rdw_typeset.replace(visions_ordinal, visions_ordinal_az)
rdw_typeset = rdw_typeset.replace(visions_categorical, visions_categorical_str)


if __name__ == "__main__":
    rdw_typeset.output_graph("figures/rdw_typeset.svg")
