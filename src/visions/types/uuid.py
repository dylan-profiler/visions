import uuid
from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion.test_utils import coercion_true_test
from visions.utils.series_utils import (
    isinstance_attrs,
    nullable_series_contains,
    series_not_empty,
)


def string_is_uuid(series, state: dict) -> bool:
    def f(s):
        return s.apply(uuid.UUID)

    return coercion_true_test(f)(series)


def to_uuid(series: pd.Series, state: dict) -> pd.Series:
    return series.apply(uuid.UUID)


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import Object, String

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls, String, relationship=string_is_uuid, transformer=to_uuid
        ),
    ]
    return relations


class UUID(VisionsBaseType):
    """**UUID** implementation of :class:`visions.types.type.VisionsBaseType`.

    References:
        UUID specification in RFC4122:
        https://tools.ietf.org/html/rfc4122#section-3

        Python standard library:
        https://docs.python.org/3/library/uuid.html

    Examples:
        >>> import pandas as pd
        >>> import uuid
        >>> uuids = ['0b8a22ca-80ad-4df5-85ac-fa49c44b7ede', 'aaa381d6-8442-4f63-88c8-7c900e9a23c6']
        >>> x = pd.Series([uuid.UUID(uuid_str) for uuid_str in uuids])
        >>> x in visions.UUID
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations(cls)

    @classmethod
    @series_not_empty
    @nullable_series_contains
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        return isinstance_attrs(series, uuid.UUID, ["time_low", "hex"])
