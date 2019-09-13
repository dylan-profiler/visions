from functools import wraps


def unique_summary(func):
    """Mixin adding missing value support to tenzing types

    When creating a custom Tenzing type simply inherit from optionMixin to add
    automatic support for missing values.

    """

    @wraps(func)
    def summarization_op(cls, series):
        summary = {}

        # try:
        n_unique = len(set(series.values))
        # n_unique = series.nunique()
        summary.update(
            {"n_unique": n_unique, "perc_unique": float(n_unique) / len(series)}
        )
        # except Exception:
        #     pass
        summary.update(func(cls, series))
        return summary

    return summarization_op


def unique_warnings(func):
    def warnings(cls, summary):
        messages = []
        if summary["n_unique"] == 1:
            messages.append("n_unique:const")
        if summary["p_unique"] == 1.0:
            messages.append("n_unique:unique")
        return messages

    return warnings
