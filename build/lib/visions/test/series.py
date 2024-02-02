from typing import Dict

import pandas as pd


def get_series() -> Dict[str, pd.Series]:
    from visions.backends.numpy.sequences import get_sequences as get_numpy_sequences
    from visions.backends.pandas.sequences import get_sequences as get_pandas_sequences
    from visions.backends.python.sequences import get_sequences as get_builtin_sequences

    sequences = get_builtin_sequences()
    sequences.update(get_numpy_sequences())

    test_series = {name: pd.Series(sequence) for name, sequence in sequences.items()}
    test_series.update(get_pandas_sequences())
    assert all(isinstance(v, pd.Series) for v in test_series.values())

    return test_series
