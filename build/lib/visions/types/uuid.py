from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.object import Object
from visions.types.string import String
from visions.types.type import VisionsBaseType


class UUID(VisionsBaseType):
    """**UUID** implementation of :class:`visions.types.type.VisionsBaseType`.

    References:
        UUID specification in RFC4122:
        https://tools.ietf.org/html/rfc4122#section-3

        Python standard library:
        https://docs.python.org/3/library/uuid.html

    Examples:
        >>> import uuid
        >>> import visions
        >>> uuids = ['0b8a22ca-80ad-4df5-85ac-fa49c44b7ede', 'aaa381d6-8442-4f63-88c8-7c900e9a23c6']
        >>> x = [uuid.UUID(uuid_str) for uuid_str in uuids]
        >>> x in visions.UUID
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(Object),
            InferenceRelation(String),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass
