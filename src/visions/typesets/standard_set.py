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
)
from visions.typesets.typeset import VisionsTypeset


class StandardSet(VisionsTypeset):
    """The standard visions typesets

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
        }
        super().__init__(types)
