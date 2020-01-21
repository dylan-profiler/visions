from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport

import seaborn as sns
import matplotlib.pyplot as plt
from visions.core import type_cast_frame

from examples.data_compression.rdw_typeset import rdw_typeset


def get_file_size(file_name: Path):
    return file_name.stat().st_size


def benchmark_sizes(file_name):
    # Benchmark for raw data sizes (not interested in compression times)

    sizes = []
    data_path = Path("data")
    for n in [100, 1000, 10000, 100000, 1000000]:  # None
        df = pd.read_csv(file_name, nrows=n)
        # cast_df = type_cast_frame(df, rdw_typeset)
        #
        # size_1 = get_df_size(df)
        # size_2 = get_df_size(cast_df)
        # if ratio:
        #     size_2 = size_2 / size_1
        #     size_1 = 1.0
        #
        # sizes.append({"size": size_1, "type": "DataFrame", "n": n})
        # sizes.append({"size": size_2, "type": "DataFrame (after cast)", "n": n})

        csv_path = data_path / file_name.with_suffix(f".{n}.csv").name
        if not csv_path.exists():
            df.to_csv(csv_path, index=False)
        sizes.append({"size": get_file_size(csv_path), "type": "csv", "n": n})

        parquet_path = data_path / file_name.with_suffix(f".{n}.parquet").name
        if not parquet_path.exists():
            df.to_parquet(parquet_path)
        sizes.append({"size": get_file_size(parquet_path), "type": "parquet", "n": n})

        # https://stackoverflow.com/questions/46906889/how-to-store-null-value-in-hdf5-table
        h5_path = data_path / file_name.with_suffix(f".{n}.h5").name
        if not h5_path.exists():
            df.to_hdf(h5_path, key="rdw")
        sizes.append({"size": get_file_size(h5_path), "type": "h5", "n": n})

        pickle_path = data_path / file_name.with_suffix(f".{n}.pickle").name
        if not pickle_path.exists():
            df.to_pickle(pickle_path)
        sizes.append({"size": get_file_size(pickle_path), "type": "pickle", "n": n})

        feather_path = data_path / file_name.with_suffix(f".{n}.feather").name
        if not feather_path.exists():
            df.to_feather(feather_path)
        sizes.append({"size": get_file_size(feather_path), "type": "feather", "n": n})

    sizes_df = pd.DataFrame(sizes)

    # if ratio:
    #     ax = sns.barplot(x="n", y="size", hue="type", data=sizes_df)
    #     plt.title("Relative DataFrame Memory Usage | RDW Vehicles dataset")
    #     plt.ylabel("File Usage Ratio")
    #     plt.xlabel("Number of Rows")
    #     plt.show()
    #     fig = ax.get_figure()
    #     fig.savefig(f"sizes_bar.png")
    # else:

    ax = sns.lineplot(x="n", y="size", hue="type", data=sizes_df)
    ax.set(xscale="log", yscale="log")
    plt.ylabel("File Size (bytes)")
    plt.xlabel("Number of Rows")
    plt.title(f"File Sizes | RDW Vehicles dataset")
    plt.show()
    fig = ax.get_figure()
    fig.savefig(f"figures/file_sizes.png")


if __name__ == "__main__":
    file_name = Path(
        r"C:\Users\Cees Closed\Documents\code\say-hello\data\rdw\gekentekende_voertuigen.csv"
    )
    benchmark_sizes(file_name)
