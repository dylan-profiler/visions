import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.utils.coercion.test_utils import coercion_map_test, coercion_map


def to_bool(series: pd.Series) -> pd.Series:
    return series.astype(bool)


class tenzing_bool(tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.
    >>> x = pd.Series([True, False])
    >>> x in tenzing_bool
    True
    """

    @classmethod
    def get_relations(cls) -> dict:
        from tenzing.core.model.types import tenzing_generic, tenzing_string, tenzing_integer

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            # TODO: store mapping somewhere (for alteration and DRY)
            # TODO: ensure that series.str.lower() has no side effects
            # TODO: contrib:
            #             {"j": True, "n": False},
            #             {"ja": True, "nee": False},
            tenzing_string: relation_conf(
                inferential=True,
                relationship=lambda s: coercion_map_test(
                    [
                        {"true": True, "false": False},
                        {"y": True, "n": False},
                        {"yes": True, "no": False},
                    ]
                )(s.str.lower()),
                transformer=lambda s: to_bool(
                    coercion_map(
                        [
                            {"true": True, "false": False},
                            {"y": True, "n": False},
                            {"yes": True, "no": False},
                        ]
                    )(s.str.lower())
                ),
            ),
            tenzing_integer: relation_conf(
                inferential=True,
                relationship=lambda s: set(s.unique()) == {0, 1},
                transformer=to_bool,
            ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return not pdt.is_categorical_dtype(series) and pdt.is_bool_dtype(series)
