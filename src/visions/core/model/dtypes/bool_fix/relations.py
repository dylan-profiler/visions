import pandas as pd

from visions.core.model import TypeRelation
from visions.core.implementations.types import (
    visions_bool,
    visions_string,
    visions_generic,
    visions_object,
)
from visions.utils.coercion import test_utils


def register_bool_relations():
    # Nullable bool: Object - > Bool
    class string_bool_relation:
        _boolean_maps = [
            {"true": True, "false": False},
            {"y": True, "n": False},
            {"yes": True, "no": False},
        ]

        def __init__(self):
            self._full_boolean_map = {
                k: v for d in self._boolean_maps for k, v in d.items()
            }

        # TODO: ensure that series.str.lower() has no side effects
        def string_is_bool(self, series):
            temp_series = series.str.lower()
            return any(
                temp_series.isin(boolean_map.keys()).all()
                for boolean_map in self._boolean_maps
            )

        def map_string_to_bool(self, series):
            return series.str.lower().map(self._full_boolean_map)

    sb_relation = string_bool_relation()
    relations = [
        TypeRelation(visions_bool, visions_generic, inferential=False),
        TypeRelation(
            visions_bool,
            visions_string,
            sb_relation.string_is_bool,
            sb_relation.map_string_to_bool,
            inferential=True,
        ),
        TypeRelation(
            visions_bool,
            visions_object,
            test_utils.coercion_equality_test(
                lambda s: pd.to_numeric(s).astype("Bool")
            ),
            inferential=True,
        ),
    ]
    return relations
