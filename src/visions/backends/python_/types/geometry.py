import os
import sys
from typing import Iterable

from visions.types.string import String
from visions.types.geometry import Geometry


@Geometry.register_relationship(String, Iterable)
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


@Geometry.register_transformer(String, Iterable)
def string_to_geometry(sequence: Iterable, state: dict) -> Iterable:
    from shapely import wkt

    return map(wkt.loads, sequence)


@Geometry.contains_op.register(Iterable)
def geometry_contains(sequence: Iterable, state: dict) -> bool:
    from shapely.geometry.base import BaseGeometry

    return all(issubclass(type(x), BaseGeometry) for x in sequence)
