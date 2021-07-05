from visions.types import (
    URL,
    UUID,
    Boolean,
    Categorical,
    Complex,
    Count,
    Date,
    DateTime,
    EmailAddress,
    File,
    Float,
    Generic,
    Geometry,
    Image,
    Integer,
    IPAddress,
    Object,
    Ordinal,
    Path,
    String,
    Time,
    TimeDelta,
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
    - EmailAddress
    - UUID

    """

    def __init__(self) -> None:
        types = {
            Generic,
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
            EmailAddress,
            UUID,
        }
        super().__init__(types)

        try:
            import imagehash
            import PIL
            import shapely
        except ImportError as e:
            raise ImportError(
                f"This typeset requires dependencies that are currently not installed ({e}). "
                "You can follow the installation instructions to resolve this issue: "
                "https://dylan-profiler.github.io/visions/visions/getting_started/installation.html"
            )
