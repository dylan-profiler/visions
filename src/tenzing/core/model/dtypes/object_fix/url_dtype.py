import pandas as pd
import numpy as np
from pandas.core.dtypes.base import ExtensionDtype
from urllib.parse import ParseResult

from tenzing.core.model.dtypes.url_array import UrlArray


@pd.api.extensions.register_extension_dtype
class UrlType(ExtensionDtype):
    name = 'Url'
    type = ParseResult
    kind = 'O'
    _record_type = np.dtype(np.object)
    na_value = np.nan

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from "
                            "'{}'".format(cls, string))

    @classmethod
    def construct_array_type(cls):
        return UrlArray