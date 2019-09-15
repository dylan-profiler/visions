def category_summary(series):
    summary = {
        "category_size": len(series.dtype._categories),
        "ordered": series.dtype.ordered,
    }

    summary["missing_categorical_values"] = (
        True if series.nunique() != summary["category_size"] else False
    )
    return summary
