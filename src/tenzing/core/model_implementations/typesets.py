from tenzing.core.models import tenzing_typeset, tenzing
from tenzing.core.model_implementations import *

import pandas as pd


def _get_column_names(obj):
    if isinstance(obj, pd.DataFrame):
        return obj.columns.values.tolist()
    elif isinstance(obj, list):
        return obj


class tenzing_standard(tenzing):
    def __init__(self):
        basetypes = [tenzing_bool, tenzing_float, tenzing_string, tenzing_object,
                     tenzing_complex, tenzing_categorical, tenzing_timestamp,
                     tenzing_integer]
        super().__init__(basetypes)
