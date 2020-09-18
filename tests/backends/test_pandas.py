import pandas as pd
from visions import StandardSet


def test_pandas_inference():
    abc = StandardSet()
    print(abc.infer_type(pd.Series([1, 2, 3])))