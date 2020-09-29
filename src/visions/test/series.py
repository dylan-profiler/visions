from typing import Dict

import pandas as pd


def get_series() -> Dict[str, pd.Series]:
    from visions.backends.numpy_.sequences import get_sequences as get_numpy_sequences
    from visions.backends.pandas_be.sequences import get_sequences as get_pandas_sequences
    from visions.backends.python_.sequences import get_sequences as get_builtin_sequences

    sequences = get_builtin_sequences()
    sequences.update(get_numpy_sequences())

    test_series = {name: pd.Series(sequence) for name, sequence in sequences.items()}
    test_series.update(get_pandas_sequences())

    return test_series
