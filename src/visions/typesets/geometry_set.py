from visions.types import (
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

    def __init__(self):
        types = {
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
