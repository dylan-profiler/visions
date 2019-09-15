def base_summary(series):
    summary = {
        "frequencies": series.value_counts().to_dict(),
        "n_records": series.shape[0],
        "memory_size": series.memory_usage(index=True, deep=True),
        "dtype": series.dtype,
        "types": series.map(type).value_counts().to_dict(),
    }

    return summary
