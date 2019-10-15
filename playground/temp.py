import datetime

from visions.core.model import visions_complete_set
import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "item_id": [1, 1, 3],
        "item_cost": [2.1, 3.5, 4],
        "item_name": ["orange", "orange", "apple"],
        "sale_date": pd.to_datetime(
            [
                datetime.date(2011, 1, 1),
                datetime.date(2012, 1, 2),
                datetime.date(2013, 1, 1),
            ]
        ),
        "store_location": pd.Series(
            ["POINT (12 42)", "POINT (100 42.723)", "POINT (0 0)"]
        ),
        "COGS": pd.Series([np.nan, 1.1, 2.1]).astype(str),
        "is_still_available": [np.inf, False, True],
        "is_expired": ["True", "false", "False"],
        "is_person": ["Y", "N", "Y"],
        "website": [
            "http://www.google.com",
            "http://www.bing.com",
            "http://www.duckduckgo.com",
        ],
        "complex_record": [np.complex(1, 2), np.complex(3, 4), np.complex(5, 6)],
        "path_linux": [
            r"/home/user/test.txt",
            r"/home/user/test.bat",
            r"/home/user/test.sh",
        ],
        "path_win": [r"C:\Users\test.txt", r"C:\Users\test.bat", r"C:\Users\test.sh"],
    }
)
x = visions_complete_set()
y = visions_complete_set()
x.prep(df)
tdf = x.cast_to_inferred_types(df)

print(x.column_type_map)
y.prep(tdf)
print(y.column_type_map)
