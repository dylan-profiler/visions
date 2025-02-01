from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, TypeRelation
from visions.types.generic import Generic
from visions.types.type import VisionsBaseType


class Numeric(VisionsBaseType):
    """**Numeric** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> import visions
        >>> from decimal import Decimal
        >>>
        >>> x = [Decimal(1), Decimal(2), Decimal(3)]
        >>> x in visions.Numeric
        True
    """

    @staticmethod
    def get_relations() -> Sequence[TypeRelation]:
        relations = [IdentityRelation(Generic)]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass
