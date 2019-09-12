class optionMixin:
    """Mixin adding missing value support to tenzing types

    When creating a custom Tenzing type simply inherit from optionMixin to add
    automatic support for missing values.

    """

    is_option = True

    @classmethod
    def get_series(self, series):
        series = super().get_series(series)
        return series[series.notna()]

    @classmethod
    def cast_op(self, series, operation=None):
        operation = operation if operation is not None else super().cast_op
        notna_series = self.get_series(series)
        # TODO: copy?
        return operation(notna_series)

    @classmethod
    def contains_op(self, series, operation=None):
        notna_series = self.get_series(series)
        return super().contains_op(notna_series, operation)

    @classmethod
    def summarization_op(self, series):
        idx = series.isna()
        summary = super().summarization_op(series[~idx])

        summary["na_count"] = idx.values.sum()
        summary["perc_na"] = (
            summary["na_count"] / series.shape[0] if series.shape[0] > 0 else 0
        )
        return summary
