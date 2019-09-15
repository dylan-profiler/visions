def category_summary(series):
    summary = {"category_size": len(series.dtype._categories)}
    summary["missing_categorical_values"] = (
        True if series.nunique() != summary["category_size"] else False
    )
    summary["ordered"] = series.dtype.ordered
    return summary
