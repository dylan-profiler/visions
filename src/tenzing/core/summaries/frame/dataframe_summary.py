import pandas as pd


# TODO: add `n_cells_missing`
# TODO: add `p_cells_missing`
# TODO: add `n_vars_with_missing`
# TODO: add `type frequencies`
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
        "memory_size": df.memory_usage(index=True, deep=True).sum(),
    }
