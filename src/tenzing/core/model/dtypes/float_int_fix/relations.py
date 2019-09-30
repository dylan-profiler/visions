import pandas as pd


from tenzing.core.model import model_relation
from tenzing.core.model.types import (
    tenzing_integer,
    tenzing_generic,
    tenzing_float,
    tenzing_string,
)
from tenzing.utils.coercion import test_utils


def register_integer_relations():
    relations = [
        model_relation(tenzing_integer, tenzing_generic, inferential=False),
        model_relation(
            tenzing_integer,
            tenzing_float,
            test_utils.coercion_equality_test(lambda s: s.astype(int)),
            inferential=True,
        ),
        model_relation(
            tenzing_integer,
            tenzing_float,
            test_utils.coercion_equality_test(lambda s: s.astype("Int64")),
            inferential=False,
        ),
        model_relation(
            tenzing_integer,
            tenzing_string,
            test_utils.coercion_test(lambda s: s.astype(int)),
            inferential=True,
        ),
        model_relation(
            tenzing_integer,
            tenzing_string,
            test_utils.coercion_test(lambda s: pd.to_numeric(s).astype("Int64")),
            inferential=True,
        ),
    ]

    return relations
