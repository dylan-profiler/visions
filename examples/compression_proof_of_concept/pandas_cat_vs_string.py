import string
from random import choices

import pandas as pd
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport

import seaborn as sns


def generate_values(length, distinct):
    vals = set()
    while len(vals) < distinct:
        vals.add("".join(choices(string.ascii_letters, k=length)))
    return vals


n_values = [100, 1000, 10000, 100000]
distinct_values = [1, 10, 20, 50, 100]
distinct_percentages = [1, 10, 20, 50, 100]

series_sizes = []
for n in n_values:

    for dp in distinct_percentages:
        distinct = int(dp / 100.0 * n)
        for slen in [10]:
            vals = list(generate_values(slen, distinct)) * int(n / distinct)
            for t in ["str", "cat"]:
                name = f"n{n}_distinct{distinct}_t{t}"
                if t == "str":
                    encoding = "string"
                    data = pd.Series(vals)
                else:
                    encoding = "category"
                    data = pd.Series(vals, dtype="category")

                series_sizes.append(
                    {
                        "n": n,
                        "distinct_percentage": dp,
                        "size": data.memory_usage(deep=True, index=True),
                        "dtype": encoding,
                    }
                )

sizes_df = pd.DataFrame(series_sizes)

ax = sns.lineplot(x="distinct_percentage", y="size", hue="dtype", data=sizes_df)
# ax.set(xscale="log", yscale="log")
plt.ylabel("Memory Usage (bytes)")
plt.xlabel("Percentage of Unique Values")
plt.title("Memory Usage for category and string")
plt.show()
fig = ax.get_figure()
fig.savefig("category_string_memory.png")
