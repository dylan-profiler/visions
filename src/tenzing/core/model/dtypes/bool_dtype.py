import pandas as pd
from pandas import Int8Dtype


@pd.api.extensions.register_extension_dtype
class Bool(Int8Dtype):
    name = "Bool"
    # TODO: overload dtype Int8 name...