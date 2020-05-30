from visions import VisionsTypeset
from visions.types.qualitative_quantitative import (
    Continuous,
    Discrete,
    Nominal,
    Ordinal,
    Qualitative,
    Quantitative,
)


class QualitativeQuantitativeSet(VisionsTypeset):
    """Statistical typeset classified by qualitative/quantitative.

    Includes support for the following types:
    - Quantitative
    - Qualitative
    - Continuous
    - Discrete
    - Ordinal
    - Nominal
    """

    def __init__(self):
        types = {Nominal, Ordinal, Discrete, Continuous, Quantitative, Qualitative}
        super().__init__(types)
