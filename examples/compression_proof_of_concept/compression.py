from pathlib import Path

import pandas as pd
import numpy as np
from pandas import CategoricalDtype
from pandas_profiling import ProfileReport

from visions.core.implementations import visions_complete_set
from visions.core.functional import type_cast_frame, type_inference_frame
from visions.application.summaries.summary import CompleteSummary

import seaborn as sns
import matplotlib.pyplot as plt

# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
from examples.compression_proof_of_concept.rdw_typeset import rdw_typeset

file_name = Path(
    r"C:\Users\Cees Closed\Downloads\Open_Data_RDW__Gekentekende_voertuigen.csv"
)


def get_file_size(file_name: Path):
    return file_name.stat().st_size


def get_df_size(df: pd.DataFrame):
    return df.memory_usage(deep=True).sum()


# Load dataset
# df = pd.read_csv(file_name, nrows=1000)


def benchmark_sizes():
    # TODO: Benchmark raw data sizes (not interested in compression times)
    sizes = []
    for n in [100, 1000, 10000, 100000, 1000000]:  # None
        df = pd.read_csv(file_name, nrows=n)

        csv_path = Path(file_name.with_suffix(f".{n}.csv").name)
        if not csv_path.exists():
            df.to_csv(csv_path, index=False)
        sizes.append({"size": get_file_size(csv_path), "type": "csv", "n": n})

        parquet_path = Path(file_name.with_suffix(f".{n}.parquet").name)
        if not parquet_path.exists():
            df.to_parquet(parquet_path)
        sizes.append({"size": get_file_size(parquet_path), "type": "parquet", "n": n})

        # https://stackoverflow.com/questions/46906889/how-to-store-null-value-in-hdf5-table
        h5_path = Path(file_name.with_suffix(f".{n}.h5").name)
        if not h5_path.exists():
            df.to_hdf(h5_path, key="rdw")
        sizes.append({"size": get_file_size(h5_path), "type": "h5", "n": n})

        pickle_path = Path(file_name.with_suffix(f".{n}.pickle").name)
        if not pickle_path.exists():
            df.to_pickle(pickle_path)
        sizes.append({"size": get_file_size(pickle_path), "type": "pickle", "n": n})

        feather_path = Path(file_name.with_suffix(f".{n}.feather").name)
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


benchmark_sizes()
exit()
# TODO: Plot sizes

# Type
typeset = rdw_typeset

# Type inference
inferred_types = type_inference_frame(df, typeset)
print(inferred_types)

# Type cast
cast_df = type_cast_frame(df, typeset)

# Summarization
# summary = CompleteSummary()
# summaries = summary.summarize(cast_df, inferred_types)
# for key, variable_summary in summaries["series"].items():
#     print(key, variable_summary)

og_subset_name = file_name.parent / "subset.csv"
df.to_csv(og_subset_name, index=False)

new_name = file_name.parent / "blaat.csv"
cast_df.to_csv(new_name, index=False)

manual_name = file_name.parent / "manual.csv"
manual_df = df.copy(deep=True)
# TODO: compress


# print(manual_df['Zuinigheidslabel'].memory_usage(deep=True))
# print(manual_df['Zuinigheidslabel'].memory_usage(deep=True))

# Ordinal with low cardinality
def compress_integer(series):
    series_min = series.min()
    series_max = series.max()
    nans = series.dtype
    print(nans)

    t = ""
    if series_min >= 0:
        t += "U"


# TODO: if unique < 50% -> categorical encoding
manual_df["Zuinigheidslabel"] = manual_df["Zuinigheidslabel"].astype(
    CategoricalDtype(categories=["A", "B", "C", "D", "E", "F", "G"], ordered=True)
)
compress_integer(cast_df["Aantal rolstoelplaatsen"])
manual_df["Aantal rolstoelplaatsen"] = manual_df["Aantal rolstoelplaatsen"].astype(
    "UInt8"
)
manual_df["Aantal deuren"] = manual_df["Aantal deuren"].astype("UInt8")
manual_df["Wielbasis"] = manual_df["Wielbasis"].astype("UInt16")
manual_df["Cilinderinhoud"] = manual_df["Cilinderinhoud"].astype("UInt16")
manual_df["Breedte"] = manual_df["Breedte"].astype("UInt16")
manual_df["Toegestane maximum massa voertuig"] = manual_df[
    "Toegestane maximum massa voertuig"
].astype("UInt32")
manual_df["Catalogusprijs"] = manual_df["Catalogusprijs"].astype("UInt32")
manual_df["WAM verzekerd"] = manual_df["WAM verzekerd"].astype(
    "category"
)  # TODO: possibly boolean
manual_df["Wacht op keuren"] = manual_df["Wacht op keuren"].astype("category")
manual_df["Type gasinstallatie"] = manual_df["Type gasinstallatie"].astype("category")
manual_df["Voertuigsoort"] = manual_df["Voertuigsoort"].astype("category")
manual_df["Eerste kleur"] = manual_df["Eerste kleur"].astype("category")
manual_df["Tweede kleur"] = manual_df["Tweede kleur"].astype("category")
manual_df["Inrichting"] = manual_df["Inrichting"].astype("category")
manual_df["Volgnummer wijziging EU typegoedkeuring"] = manual_df[
    "Volgnummer wijziging EU typegoedkeuring"
].astype("UInt8")
manual_df["Vervaldatum APK"] = pd.to_datetime(
    manual_df["Vervaldatum APK"], format="%Y%m%d"
)
manual_df["Datum tenaamstelling"] = pd.to_datetime(
    manual_df["Datum tenaamstelling"], format="%Y%m%d"
)
manual_df["Datum eerste toelating"] = pd.to_datetime(
    manual_df["Datum eerste toelating"], format="%Y%m%d"
)
manual_df["Vervaldatum tachograaf"] = pd.to_datetime(
    manual_df["Vervaldatum tachograaf"], format="%Y%m%d"
)

manual_df.to_csv(manual_name, index=False)

profile = ProfileReport(manual_df)
profile.to_file("cleaned.html", silent=False)

parq = get_file_size(file_name.with_suffix(".parquet"))
og_size = get_file_size(og_subset_name)
cast_size = get_file_size(new_name)
manual_size = get_file_size(manual_name)

# Compare file sizes
print(f"Original file: {og_size}", get_df_size(df))
print(
    f"Manual file: {manual_size}, reduction of {100 - (manual_size / og_size * 100)}",
    get_df_size(manual_df),
)
print(
    f"Cast file: {cast_size}, reduction of {100 - (cast_size / og_size * 100)}",
    get_df_size(cast_df),
)
print(f"Parquet file: {parq}, reduction of {100 - (parq / og_size * 100)}")

encodings = {
    "csv": lambda df: df.to_csv,
    "parquet": lambda df: df.to_parquet,
    "pickle": lambda df: df.to_pickle,
    "hdf": lambda df: df.to_hdf,
    "df": lambda df: lambda x: x,
}
