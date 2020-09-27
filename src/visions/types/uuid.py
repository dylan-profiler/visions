import uuid
from multimethod import multimethod
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


def string_is_uuid(item: str, state: dict) -> bool:
    try:
        _ = string_to_uuid(item)
        return True
    except:
        return False


def string_to_uuid(item: str, state: dict) -> Iterable:
    return uuid.UUID(item)


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
    @multimethod
    def contains_op(sequence: uuid.UUID, state: dict):
        return True

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        from visions.types import Object, String

        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls, String, relationship=string_is_uuid, transformer=string_to_uuid
            ),
        ]
        return relations