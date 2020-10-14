from typing import Any, Sequence

from multimethod import multimethod

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.object import Object
from visions.types.string import String
from visions.types.type import VisionsBaseType


class Geometry(VisionsBaseType):
    """**Geometry** implementation of :class:`visions.types.type.VisionsBaseType`.

    Examples:
        >>> from shapely import wkt
        >>> x = pd.Series([wkt.loads('POINT (-92 42)'), wkt.loads('POINT (-92 42.1)'), wkt.loads('POINT (-92 42.2)')]
        >>> x in visions.geometry
        True
    """

    @classmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls,
                String,
            ),
        ]
        return relations

    @staticmethod
    @multimethod
    def contains_op(item: Any, state: dict) -> bool:
        pass
