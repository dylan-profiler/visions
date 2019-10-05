import pandas.api.types as pdt
import pandas as pd

from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.models import tenzing_model
from tenzing.utils.coercion import test_utils


def string_to_int(series: pd.Series) -> pd.Series:
    return to_int(series.astype(float))


def to_int(series: pd.Series) -> pd.Series:
    try:
        return series.astype(int)
    except TypeError:
        return series.astype("Int64")


class tenzing_integer(tenzing_model):
    """**Integer** implementation of :class:`tenzing.core.models.tenzing_model`.

    Examples:
        >>> x = pd.Series([1, 2, 3])
        >>> x in tenzing_integer
        True
    """

    @classmethod
    def get_relations(cls):
        from tenzing.core.model.types import tenzing_string, tenzing_generic, tenzing_float

        relations = {
            tenzing_generic: relation_conf(inferential=False),
            tenzing_float: relation_conf(
                relationship=test_utils.coercion_equality_test(to_int),
                transformer=to_int,
                inferential=True,
            ),
            tenzing_string: relation_conf(
                relationship=test_utils.coercion_test(string_to_int),
                transformer=string_to_int,
                inferential=True,
            ),
        }

        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_signed_integer_dtype(series)
