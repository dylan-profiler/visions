def base_summary(func):
    """Mixin adding missing value support to tenzing types

    When creating a custom Tenzing type simply inherit from optionMixin to add
    automatic support for missing values.

    """
    def summarization_op(self, series):
        summary = {
            'frequencies': series.value_counts().to_dict(),
            'n_records': series.shape[0],
            'memory_size': series.memory_usage(index=True, deep=True),

            'dtype': series.dtype,
            'types': series.map(type).value_counts().to_dict()
        }
        return summary
    return summarization_op