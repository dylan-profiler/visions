# TODO: rename to reflect contents of summary
def complex_summary(series):
    aggregates = ["mean", "std", "var", "min", "max", "sum"]
    summary = series.agg(aggregates).to_dict()
    return summary
