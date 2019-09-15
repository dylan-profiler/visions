def dataframe_summary(df):
    return {
        "n_observations": df.shape[0],
        "n_variables": df.shape[1],
        "memory_size": df.memory_usage(index=True, deep=True).sum(),
    }
