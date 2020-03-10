import pandas as pd


def dataframe_summary(df: pd.DataFrame) -> dict:
    """Summarization for a DataFrame

    Args:
        df: a DataFrame object to summarize

    Returns:
        Summary of the DataFrame with `n_observations`, `n_variables` and `memory_size`.
    """
    return {
        "n_observations": df.shape[0],
        "n_variables": df.shape[1],
        "memory_size": df.memory_usage(deep=True).sum(),
    }
