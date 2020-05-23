from typing import Sequence

import pandas as pd

from visions.relations import IdentityRelation, InferenceRelation, TypeRelation
from visions.types.type import VisionsBaseType
from visions.utils.coercion import test_utils
from visions.utils.warning_handling import discard_stderr


def to_geometry(series: pd.Series) -> pd.Series:
    from shapely import wkt

    return pd.Series([wkt.loads(value) for value in series])


def _get_relations(cls) -> Sequence[TypeRelation]:
    from visions.types import String, Object
    from shapely.errors import WKTReadingError

    relations = [
        IdentityRelation(cls, Object),
        InferenceRelation(
            cls,
            String,
            relationship=test_utils.coercion_test(
                discard_stderr(to_geometry), [WKTReadingError, UnicodeEncodeError]
            ),
            transformer=to_geometry,
        ),
    ]
    return relations


# https://jorisvandenbossche.github.io/blog/2019/08/13/geopandas-extension-array-refactor/
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
        return _get_relations(cls)

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        from shapely.geometry.base import BaseGeometry

        return all(issubclass(type(x), BaseGeometry) for x in series)
