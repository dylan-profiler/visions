import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins import uniqueSummaryMixin, optionMixin, baseSummaryMixin
from tenzing.utils import singleton
from tenzing.utils.unicodedata2 import script_cat


@singleton.singleton_object
class tenzing_string(baseSummaryMixin, optionMixin, uniqueSummaryMixin, tenzing_model):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 'b', np.nan])
    >>> x in tenzing_string
    True
    """
    def contains_op(self, series):
        if not pdt.is_object_dtype(series):
            return False

        return series.eq(series.astype(str)).all()

    def cast_op(self, series):
        return series.astype(str)

    def summarization_op(self, series):
        summary = super().summarization_op(series)

        # Distribution of length
        summary["length"] = series.map(lambda x: len(str(x))).value_counts().to_dict()

        # Unicode Scripts and Categories
        unicode_series = series.apply(lambda sequence: {script_cat(character) for character in sequence})
        unicode_scripts = {y for x in unicode_series.values for y in x}
        summary['unicode_scripts'] = unicode_scripts

        return summary
