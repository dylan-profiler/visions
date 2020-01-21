from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport

import seaborn as sns
import matplotlib.pyplot as plt
from visions.core import type_cast_frame

from examples.data_compression.rdw_typeset import rdw_typeset


def get_df_size(df: pd.DataFrame):
    return df.memory_usage(deep=True).sum()


def benchmark_sizes(file_name, ratio=False):
    # Benchmark for raw data sizes (not interested in compression times)

    sizes = []
    for n in [100, 1000, 10000, 100000, 1000000]:  # None
        df = pd.read_csv(file_name, nrows=n)
        cast_df = type_cast_frame(df, rdw_typeset)

        size_1 = get_df_size(df)
        size_2 = get_df_size(cast_df)
        if ratio:
            size_2 = size_2 / size_1
            size_1 = 1.0

        sizes.append({"size": size_1, "type": "DataFrame", "n": n})
        sizes.append({"size": size_2, "type": "DataFrame (after cast)", "n": n})

    sizes_df = pd.DataFrame(sizes)

    if ratio:
        ax = sns.barplot(x="n", y="size", hue="type", data=sizes_df)
        plt.title("Relative DataFrame Memory Usage | RDW Vehicles dataset")
        plt.ylabel("Memory Usage Ratio")
        plt.xlabel("Number of Rows")
        plt.show()
        fig = ax.get_figure()
        fig.savefig(f"figures/memory_usage_ratio.png")
    else:
        ax = sns.lineplot(
            x="n", y="size", hue="type", data=sizes_df[sizes_df.type == "DataFrame"]
        )
        ax.set(xscale="log", yscale="log")
        plt.ylabel("Memory Used (bytes)")
        plt.xlabel("Number of Rows")
        plt.title(f"Memory Usage | RDW Vehicles dataset")
        plt.show()
        fig = ax.get_figure()
        fig.savefig(f"figures/memory_usage.png")

        ax = sns.lineplot(x="n", y="size", hue="type", data=sizes_df)
        ax.set(xscale="log", yscale="log")
        plt.ylabel("Memory Used (bytes)")
        plt.xlabel("Number of Rows")
        plt.title(f"Memory Usage | RDW Vehicles dataset")
        plt.show()
        fig = ax.get_figure()
        fig.savefig(f"figures/memory_usage_compare.png")


if __name__ == "__main__":
    file_name = Path(
        r"C:\Users\Cees Closed\Documents\code\say-hello\data\rdw\gekentekende_voertuigen.csv"
    )
    benchmark_sizes(file_name, ratio=False)
    benchmark_sizes(file_name, ratio=True)
