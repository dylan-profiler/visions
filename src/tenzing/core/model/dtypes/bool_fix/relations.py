import pandas as pd

from tenzing.core.model import model_relation
from tenzing.core.model.types import tenzing_bool, tenzing_string, tenzing_generic, tenzing_object
from tenzing.utils.coercion import test_utils


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
        model_relation(tenzing_bool, tenzing_generic, inferential=False),
        model_relation(
            tenzing_bool,
            tenzing_string,
            sb_relation.string_is_bool,
            sb_relation.map_string_to_bool,
            inferential=True,
        ),
        model_relation(
            tenzing_bool,
            tenzing_object,
            test_utils.coercion_equality_test(lambda s: pd.to_numeric(s).astype('Bool')),
            inferential=True
        )
    ]
    return relations