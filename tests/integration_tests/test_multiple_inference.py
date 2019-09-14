#!/usr/bin/env python
# coding: utf-8
from pprint import pprint

import pandas as pd
import numpy as np
import datetime

from tenzing.core.model_implementations.typesets import tenzing_complete_set


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
        "is_still_available": [True, False, True],
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

ts = tenzing_complete_set()
ts.prep(df)

print("initial types")
initial_types = ts.column_type_map
pprint(initial_types)

summary = ts.summary_report(df)

print("inferred types")
inferred_types = ts.infer_types(df)
pprint(inferred_types)

df_clean = ts.cast_to_inferred_types(df)

print("inferred types after convert")
inferred_types_cast = ts.infer_types(df_clean)
pprint(inferred_types_cast)

for key, type in inferred_types.items():
    assert type == inferred_types_cast[key], f'cast type {inferred_types_cast[key]} \
                                              does not match inferred type {type} for series {key}'
