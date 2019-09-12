class optionMixin:
    """Mixin adding missing value support to tenzing types

    When creating a custom Tenzing type simply inherit from optionMixin to add
    automatic support for missing values.
    """

    @classmethod
    def get_series(cls, series):
        series = super().get_series(series)
        return series[series.notna()]

    @classmethod
    def cast_op(cls, series, operation=None):
        operation = operation if operation is not None else super().cast_op
        notna_series = cls.get_series(series)
        # TODO: copy?
        return operation(notna_series)

    @classmethod
    def contains_op(cls, series):
        notna_series = cls.get_series(series)
        return super().contains_op(notna_series)

    @classmethod
    def summarization_op(cls, series):
        idx = series.isna()
        summary = super().summarization_op(series[~idx])

        summary["na_count"] = idx.values.sum()
        summary["perc_na"] = (
            summary["na_count"] / series.shape[0] if series.shape[0] > 0 else 0
        )
        return summary
