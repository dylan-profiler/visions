def zero_summary(func):
    """Mixin adding missing value support to tenzing types

    When creating a custom Tenzing type simply inherit from optionMixin to add
    automatic support for missing values.

    """

    def summarization_op(self, series):
        summary = {"n_zeros": (series == 0).sum()}
        summary["perc_zeros"] = summary["n_zeros"] / len(series)
        return summary

    return summarization_op


def zero_warnings(func):
    def warnings(summary):
        messages = []
        if summary["n_unique"] == 1:
            messages.append("n_unique:const")
        if summary["p_unique"] == 1.0:
            messages.append("n_unique:unique")
        return messages

    return warnings
