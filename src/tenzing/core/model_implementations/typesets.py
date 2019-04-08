from tenzing.core.typesets import tenzingTypeset
from tenzing.core.model_implementations import *

import pandas as pd


def _get_column_names(obj):
    if isinstance(obj, pd.DataFrame):
        return obj.columns.values.tolist()
    elif isinstance(obj, list):
        return obj


class tenzing_standard(tenzingTypeset):
    def __init__(self):
        root_types = [tenzing_bool, tenzing_float, tenzing_object,
                      tenzing_complex, tenzing_categorical, tenzing_timestamp,
                      tenzing_integer]
        derivative_types = [tenzing_string]
        super().__init__(root_types, derivative_types)
