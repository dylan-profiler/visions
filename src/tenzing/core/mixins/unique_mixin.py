class uniqueSummaryMixin:
    """Mixin adding missing value support to tenzing types

    When creating a custom Tenzing type simply inherit from optionMixin to add
    automatic support for missing values.

    """

    def get_series(self, series):
        return series

    def summarization_op(self, series):
        n_unique = len(set(series.values))
        return {"n_unique": n_unique, "perc_unique": float(n_unique) / len(series)}


"""
    def warnings(summary):
        messages = []
        if summary["n_unique"] == 1:
            messages.append("n_unique:const")
        if summary["p_unique"] == 1.0:
            messages.append("n_unique:unique")
        return messages
"""
