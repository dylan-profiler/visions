from visions import VisionsTypeset
from visions.types.measurement_level import Interval, Nominal, Ordinal, Ratio


class MeasurementLevelSet(VisionsTypeset):
    """Typeset for statistical variables as introduced by Stevens in the '40s

    Includes support for the following types:
    - Nominal
    - Ordinal
    - Interval
    - Ratio
    """

    def __init__(self):
        types = {Nominal, Ordinal, Interval, Ratio}
        super().__init__(types)
