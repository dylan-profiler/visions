import numpy as np
import pandas as pd

from visions.functional import cast_to_inferred, detect_type, infer_type
from visions.typesets import CompleteSet

# Create a DataFrame from our data
df = pd.DataFrame(
    {
        "numbers_with_nan": [3, 7, np.nan],
        "url": [
            "http://www.cwi.nl:80/%7Eguido/Python.html",
            "https://numpy.org/",
            "https://github.com/pandas-profiling/pandas-profiling",
        ],
        "uuid": [
            "0b8a22ca-80ad-4df5-85ac-fa49c44b7ede",
            "aaa381d6-8442-4f63-88c8-7c900e9a23c6",
            "00000000-0000-0000-0000-000000000000",
        ],
    }
)


# Choose the complete typeset, which includes URLs
typeset = CompleteSet()


# Detect the type (without casting)
print(detect_type(df, typeset))
# {'numbers_with_nan': Float, 'url': String, 'uuid': String}

# Cast the dataframe to inferred types
cast_df = cast_to_inferred(df, typeset)
print(cast_df.to_string())
#    numbers_with_nan                                                url                                  uuid
# 0                 3  (http, www.cwi.nl:80, /%7Eguido/Python.html, ,...  0b8a22ca-80ad-4df5-85ac-fa49c44b7ede
# 1                 7                        (https, numpy.org, /, , , )  aaa381d6-8442-4f63-88c8-7c900e9a23c6
# 2               NaN  (https, github.com, /pandas-profiling/pandas-p...  00000000-0000-0000-0000-000000000000

# Print the inferred types
print(infer_type(df, typeset))
# {'numbers_with_nan': Integer, 'url': URL, 'uuid': UUID}
