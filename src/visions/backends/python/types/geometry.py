import os
from collections.abc import Sequence
from contextlib import redirect_stderr

from visions.types.geometry import Geometry
from visions.types.string import String

try:
    from shapely.errors import ShapelyError
except ImportError:
    from shapely.errors import WKTReadingError as ShapelyError


@Geometry.register_relationship(String, Sequence)
def string_is_geometry(sequence: Sequence, state: dict) -> bool:
    """Shapely logs failures at a silly severity, just trying to suppress it's output on failures."""
    from shapely import wkt

    # only way to get rid of sys output when wkt.loads hits a bad value
    # TODO: use coercion wrapper for this
    with open(os.devnull, "w") as devnull, redirect_stderr(devnull):
        try:
            result = all(wkt.loads(value) for value in sequence)
        except (ShapelyError, AttributeError, UnicodeEncodeError, TypeError):
            result = False
    return result


@Geometry.register_transformer(String, Sequence)
def string_to_geometry(sequence: Sequence, state: dict) -> Sequence:
    from shapely import wkt

    return tuple(map(wkt.loads, sequence))


@Geometry.contains_op.register
def geometry_contains(sequence: Sequence, state: dict) -> bool:
    from shapely.geometry.base import BaseGeometry

    return all(issubclass(type(x), BaseGeometry) for x in sequence)
