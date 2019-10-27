import pandas as pd


from visions.core.model import model_relation
from visions.core.implementations.types import (
    visions_integer,
    visions_generic,
    visions_float,
    visions_string,
)
from visions.utils.coercion import test_utils


def register_integer_relations():
    relations = [
        model_relation(visions_integer, visions_generic, inferential=False),
        model_relation(
            visions_integer,
            visions_float,
            test_utils.coercion_equality_test(lambda s: s.astype(int)),
            inferential=True,
        ),
        model_relation(
            visions_integer,
            visions_float,
            test_utils.coercion_equality_test(lambda s: s.astype("Int64")),
            inferential=False,
        ),
        model_relation(
            visions_integer,
            visions_string,
            test_utils.coercion_test(lambda s: s.astype(int)),
            inferential=True,
        ),
        model_relation(
            visions_integer,
            visions_string,
            test_utils.coercion_test(lambda s: pd.to_numeric(s).astype("Int64")),
            inferential=True,
        ),
    ]

    return relations
