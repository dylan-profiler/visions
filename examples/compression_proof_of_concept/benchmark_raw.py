from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport

import seaborn as sns
import matplotlib.pyplot as plt


def get_file_size(file_name: Path):
    return file_name.stat().st_size


def get_df_size(df: pd.DataFrame):
    return df.memory_usage(deep=True).sum()


def benchmark_sizes(file_name):
    # Benchmark for raw data sizes (not interested in compression times)
    sizes = []
    data_path = Path("data")
    for n in [100, 1000, 10000, 100000, 1000000]:  # None
        df = pd.read_csv(file_name, nrows=n)

        sizes.append({"size": get_df_size(df), "type": "DataFrame in memory", "n": n})

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

    ax = sns.lineplot(x="n", y="size", hue="type", data=sizes_df)
    ax.set(xscale="log", yscale="log")
    plt.ylabel("size (bytes)")
    plt.xlabel("number of rows")
    plt.title("File sizes for stored rows | Uncompressed | RDW Vehicles dataset")
    plt.show()
    fig = ax.get_figure()
    fig.savefig("file_sizes.png")


def benchmark_uncompressed():
    file_name = Path(
        r"C:\Users\Cees Closed\Downloads\Open_Data_RDW__Gekentekende_voertuigen.csv"
    )
    benchmark_sizes(file_name)


if __name__ == "__main__":
    benchmark_uncompressed()
