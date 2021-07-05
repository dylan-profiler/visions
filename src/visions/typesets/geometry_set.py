from visions.types import (
    Boolean,
    Categorical,
    Complex,
    DateTime,
    Float,
    Generic,
    Geometry,
    Integer,
    Object,
    String,
    TimeDelta,
)
from visions.typesets.typeset import VisionsTypeset


class GeometrySet(VisionsTypeset):
    """Standard visions typeset with shapely geometry support

    Includes support for the following types:

    - Float
    - Integer
    - Boolean
    - Object
    - String
    - Complex
    - Categorical
    - DateTime
    - TimeDelta
    - Geometry

    """

    def __init__(self) -> None:
        types = {
            Generic,
            Boolean,
            Float,
            Object,
            Complex,
            Categorical,
            DateTime,
            TimeDelta,
            Integer,
            String,
            Geometry,
        }
        super().__init__(types)

        try:
            import shapely
        except ImportError as e:
            raise ImportError(
                f"This typeset requires dependencies that are currently not installed ({e}). "
                "You can follow the installation instructions to resolve this issue: "
                "https://dylan-profiler.github.io/visions/visions/getting_started/installation.html"
            )
