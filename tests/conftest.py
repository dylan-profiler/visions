import collections
from typing import Any, Iterable

import pandas as pd


def is_iter(v: Any) -> bool:
    return isinstance(v, collections.Iterable) and not isinstance(v, (str, bytes))


def sequences_equal(s1: Iterable, s2: Iterable) -> bool:
    for v1, v2 in zip(s1, s2):
        if is_iter(v1) and is_iter(v2):
            if not sequences_equal(v1, v2):
                return False
        elif not (pd.isna(v1) and pd.isna(v2)) and not v1 == v2:
            return False

    return True
