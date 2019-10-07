from urllib.parse import urlparse

import pandas as pd

from visions.core.model.dtypes.url_dtype import UrlType

# UrlType


s = pd.Series(["http://www.google.com", "http://www.ru.nl"] * 100, dtype="Url")
s2 = pd.Series(
    [urlparse("http://www.google.com"), urlparse("http://www.ru.nl")] * 100, dtype="Url"
)
s3 = pd.Series(["http://www.google.com", "http://www.ru.nl"] * 100)
s4 = pd.Series([urlparse("http://www.google.com"), urlparse("http://www.ru.nl")] * 100)


print(f"{s.memory_usage(deep=True)} bytes, {s.dtype} dtype, from string")
print(f"{s2.memory_usage(deep=True)} bytes, {s2.dtype} dtype, from ParseResult")
print(f"{s3.memory_usage(deep=True)} bytes, {s3.dtype} dtype, from string")
print(f"{s4.memory_usage(deep=True)} bytes, {s4.dtype} dtype, from ParseResult")
