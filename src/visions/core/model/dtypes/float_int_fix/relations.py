import pandas as pd


from visions.core.model import TypeRelation
from visions.core.implementations.types import (
    visions_integer,
    visions_generic,
    visions_float,
    visions_string,
)
from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.utils.coercion import test_utils


def register_integer_relations():
    relations = [
        IdentityRelation(visions_integer, visions_generic),
        InferenceRelation(
            visions_integer,
            visions_float,
            test_utils.coercion_equality_test(lambda s: s.astype(int)),
        ),
        InferenceRelation(
            visions_integer,
            visions_float,
            test_utils.coercion_equality_test(lambda s: s.astype("Int64")),
        ),
        InferenceRelation(
            visions_integer,
            visions_string,
            test_utils.coercion_test(lambda s: s.astype(int)),
        ),
        InferenceRelation(
            visions_integer,
            visions_string,
            test_utils.coercion_test(lambda s: pd.to_numeric(s).astype("Int64")),
        ),
    ]

    return relations
