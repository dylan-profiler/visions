import pandas.api.types as pdt

from tenzing.core import tenzing_model
from tenzing.core.mixins.option_mixin import optionMixin
from tenzing.utils import singleton


@singleton.singleton_object
class tenzing_bool(optionMixin, tenzing_model):
    """**Boolean** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series([True, False, np.nan])
    >>> x in tenzing_bool
    True
    """
    def contains_op(self, series):
        if pdt.is_categorical_dtype(series):
            return False
        return pdt.is_bool_dtype(series)

    def cast_op(self, series):
        return series.astype(bool)

    def summarization_op(self, series):
        summary = {}
        # TODO: common summary
        summary['frequencies'] = series.value_counts().to_dict()
        summary['n_records'] = series.shape[0]

        summary['num_True'] = summary['frequencies'].get(True, 0)
        summary['num_False'] = summary['frequencies'].get(False, 0)

        summary['perc_True'] = summary['num_True'] / summary['n_records']
        summary['perc_False'] = summary['num_False'] / summary['n_records']
        return summary
