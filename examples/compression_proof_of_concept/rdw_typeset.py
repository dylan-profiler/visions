import pandas as pd
import attr

from visions import visions_bool
from visions.core.implementations import visions_complete_set

# make Dutch boolean
from visions.lib.relations.string_to_bool import get_language_bool
from visions.lib.relations.string_to_categorical import (
    string_to_categorical_distinct_count,
)

# TODO: override visions_integer => visions_integer[xyz]
visions_bool_nl = get_language_bool("nl")

# recognizes YYYYMMDD
from visions.core.implementations.types.visions_integer import (
    _get_relations,
    visions_integer,
    to_int,
)
from visions.lib.relations.integer_to_datetime import integer_to_datetime_year_month_day


def to_int_smallest(series: pd.Series) -> pd.Series:
    max = series.max()
    min = series.min()

    if min >= 0:
        if series.hasnans:
            u = "U"
        else:
            u = "u"

        if max <= 255:
            n = 8
        elif max <= 65535:
            n = 16
        elif max <= 4294967295:
            n = 32
        else:
            n = 64
    else:
        u = ""
        if max <= 127:
            n = 8
        elif max <= 32767:
            n = 16
        elif max <= 2147483647:
            n = 32
        else:
            n = 64

    if series.hasnans:
        i = "I"
    else:
        i = "i"

    type_name = f"{u}{i}nt{n}"

    return series.astype(type_name)


@classmethod
def compose_relations_int(cls):
    # Overwrite compression
    relations = _get_relations(cls)
    new_relations = []
    for relation in relations:
        # if relation.transformer == to_int:
        #     new_relations.append(attr.evolve(relation, transformer=to_int_smallest))
        # else:
        new_relations.append(relation)
    return new_relations + [integer_to_datetime_year_month_day(cls)]


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
rdw_typeset = rdw_typeset.replace(visions_bool, visions_bool_nl)
rdw_typeset = rdw_typeset.replace(visions_integer, visions_integer_ddt)
rdw_typeset = rdw_typeset.replace(visions_categorical, visions_categorical_str)


if __name__ == "__main__":
    rdw_typeset.output_graph("rdw_typeset.svg")
