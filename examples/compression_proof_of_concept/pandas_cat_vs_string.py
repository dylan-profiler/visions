import string
from random import choices

import pandas as pd


def generate_values(length, distinct):
    vals = set()
    while len(vals) < distinct:
        vals.add("".join(choices(string.ascii_letters, k=length)))
    return vals


n_values = [100, 1000, 10000, 100000]
distinct_values = [1, 10, 20, 50, 100]
distinct_percentages = [1, 10, 20, 50, 100]

for n in n_values:
    data = {}
    for distinct in [int(dp / 100.0 * n) for dp in distinct_percentages]:
        for slen in [5, 10, 25, 50]:
            vals = list(generate_values(slen, distinct)) * int(n / distinct)
            for t in ["str", "cat"]:
                name = f"n{n}_distinct{distinct}_t{t}"
                data[name] = vals

    df = pd.DataFrame(data)
    for column in df.columns:
        if str(column).endswith("_tcat"):
            df[column] = df[column].astype("category")

        print(f"{column}, {df[column].memory_usage(deep=True, index=True)}")
