def existing_path_summary(series):
    summary = {"file_sizes": series.map(lambda x: x.stat().st_size)}
    return summary
