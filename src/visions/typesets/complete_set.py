from visions.types import (
    Boolean,
    Float,
    Object,
    Complex,
    Categorical,
    Ordinal,
    DateTime,
    TimeDelta,
    Integer,
    Count,
    String,
    Geometry,
    URL,
    Path,
    Date,
    Time,
    ExistingPath,
    ImagePath,
    IPAddress,
    UUID,
)
from visions.typesets.typeset import VisionsTypeset


class CompleteSet(VisionsTypeset):
    """Complete visions typeset with all supported types

    Includes support for the following types:

    - Float
    - Integer
    - Boolean
    - Object
    - String
    - Complex
    - Categorical
    - Ordinal
    - Count
    - DateTime
    - Date
    - Time
    - TimeDelta
    - Geometry
    - Path
    - ExistingPath
    - ImagePath
    - URL
    - IPAddress
    - UUID

    """

    def __init__(self):
        types = {
            Boolean,
            Float,
            Object,
            Complex,
            Categorical,
            Ordinal,
            DateTime,
            TimeDelta,
            Integer,
            Count,
            String,
            Geometry,
            URL,
            Path,
            Date,
            Time,
            ExistingPath,
            ImagePath,
            IPAddress,
            UUID,
        }
        super().__init__(types)
