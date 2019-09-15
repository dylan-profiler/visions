# TODO: rename to reflect contents of summary
def datetime_summary(series):
    aggregates = ["min", "max"]
    summary = series.agg(aggregates).to_dict()

    summary["range"] = summary["max"] - summary["min"]
    return summary
