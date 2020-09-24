import os
import sys
from functools import singledispatch
from typing import Iterable, Sequence

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType


@singledispatch
def string_is_geometry(sequence: Iterable, state: dict) -> bool:
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures."""
    from shapely import wkt
    from shapely.errors import WKTReadingError

    # only way to get rid of sys output when wkt.loads hits a bad value
    # TODO: use coercion wrapper for this
    sys.stderr = open(os.devnull, "w")
    try:
        result = all(wkt.loads(value) for value in sequence)
    except (WKTReadingError, AttributeError, UnicodeEncodeError, TypeError):
        result = False
    finally:
        sys.stderr = sys.__stderr__
    return result


@singledispatch
def string_to_geometry(sequence: Iterable, state: dict) -> Iterable:
    from shapely import wkt

    return map(wkt.loads, sequence)


@singledispatch
def geometry_contains(sequence: Iterable, state: dict) -> bool:
    from shapely.geometry.base import BaseGeometry

    return all(issubclass(type(x), BaseGeometry) for x in sequence)


# TODO: Evaluate https://jorisvandenbossche.github.io/blog/2019/08/13/geopandas-extension-array-refactor/
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
        from visions.types import Object, String

        relations = [
            IdentityRelation(cls, Object),
            InferenceRelation(
                cls,
                String,
                relationship=string_is_geometry,
                transformer=string_to_geometry,
            ),
        ]
        return relations

    @classmethod
    def contains_op(cls, sequence: Iterable, state: dict) -> bool:
        return geometry_contains(sequence, state)
