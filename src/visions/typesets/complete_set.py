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
    File,
    Image,
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
    - File
    - Image
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
            File,
            Image,
            IPAddress,
            UUID,
        }
        super().__init__(types)

        try:
            import shapely
            import imagehash
            import PIL
        except ImportError as e:
            raise ImportError(
                "This typeset requires dependencies that are currently not installed ({}). "
                "You can follow the installation instructions to resolve this issue: "
                "https://dylan-profiler.github.io/visions/visions/getting_started/installation.html"
                "".format(str(e))
            )
