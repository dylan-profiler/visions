import pandas.api.types as pdt
import pandas as pd

from visions.core.model.model_relation import relation_conf
from visions.core.model.type import VisionsBaseType
from visions.core.implementations.types import visions_string
from visions.utils.coercion import test_utils


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


class visions_datetime(VisionsBaseType):
    """**Datetime** implementation of :class:`visions.core.model.type.VisionsBaseType`.

    Examples:
        >>> x = pd.Series([pd.datetime(2017, 3, 5), pd.datetime(2019, 12, 4)])
        >>> x in visions_datetime
        True
    """

    @classmethod
    def get_relations(cls):
        from visions.core.implementations.types import visions_generic

        relations = {
            visions_generic: relation_conf(inferential=False),
            visions_string: relation_conf(
                relationship=test_utils.coercion_test(to_datetime),
                transformer=to_datetime,
                inferential=True,
            ),
        }
        return relations

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_datetime64_any_dtype(series)
