import uuid

import pandas as pd
from typing import Sequence

from visions.core.model.relations import IdentityRelation, InferenceRelation
from visions.core.model import TypeRelation
from visions.core.model.type import VisionsBaseType


def test_uuid(series) -> bool:
    try:
        return to_uuid(series).all()
    except (ValueError, AttributeError):
        return False


def to_uuid(series: pd.Series) -> pd.Series:
    return series.apply(lambda e: uuid.UUID(e))


def _get_relations() -> Sequence[TypeRelation]:
    from visions.core.implementations.types import visions_string, visions_object

    relations = [
        IdentityRelation(visions_uuid, visions_object),
        InferenceRelation(
            visions_uuid, visions_string, relationship=test_uuid, transformer=to_uuid
        ),
    ]
    return relations


class visions_uuid(VisionsBaseType):
    """**UUID** implementation of :class:`visions.core.model.type.VisionsBaseType`.

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
        >>> x in visions_uuid
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        return _get_relations()

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return all(isinstance(x, uuid.UUID) for x in series)
