from pathlib import Path

import pandas as pd
import numpy as np
from pandas import CategoricalDtype
from pandas_profiling import ProfileReport

from visions.core.implementations import visions_complete_set
from visions.core.functional import (
    type_cast_frame,
    type_inference_frame,
    type_detect_frame,
    compare_detect_inference_frame,
)
from visions.application.summaries.summary import CompleteSummary

# file_name = "https://opendata.rdw.nl/api/views/m9d7-ebf2/rows.csv?accessType=DOWNLOAD"
from examples.compression_proof_of_concept.rdw_typeset import rdw_typeset

file_name = Path(
    r"C:\Users\Cees Closed\Downloads\Open_Data_RDW__Gekentekende_voertuigen.csv"
)

# Load dataset
df = pd.read_csv(file_name, nrows=1000)

# Type
typeset = rdw_typeset

# Type inference
detected_types = type_detect_frame(df, typeset)
inferred_types = type_inference_frame(df, typeset)

for column, type_before, type_after in compare_detect_inference_frame(df, typeset):
    # if 'datum' in column.lower():
    changed = type_before != type_after
    if changed:
        fill = "!="
    else:
        fill = "=="
    print(f"{column: <50} {str(type_before): <16} {fill} {str(type_after): <16} ")

exit()

# Type cast
cast_df = type_cast_frame(df, typeset)

# Summarization
# summary = CompleteSummary()
# summaries = summary.summarize(cast_df, inferred_types)
# for key, variable_summary in summaries["series"].items():
#     print(key, variable_summary)

new_name = "data/cast_df.csv"
cast_df.to_csv(new_name, index=False)

# manual_name = "data/manual.csv"
# manual_df = df.copy(deep=True)


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
# manual_df["Zuinigheidslabel"] = manual_df["Zuinigheidslabel"].astype(
#     CategoricalDtype(categories=["A", "B", "C", "D", "E", "F", "G"], ordered=True)
# )
# compress_integer(cast_df["Aantal rolstoelplaatsen"])
# manual_df["Aantal rolstoelplaatsen"] = manual_df["Aantal rolstoelplaatsen"].astype(
#     "UInt8"
# )
# manual_df["Aantal deuren"] = manual_df["Aantal deuren"].astype("UInt8")
# manual_df["Wielbasis"] = manual_df["Wielbasis"].astype("UInt16")
# manual_df["Cilinderinhoud"] = manual_df["Cilinderinhoud"].astype("UInt16")
# manual_df["Breedte"] = manual_df["Breedte"].astype("UInt16")
# manual_df["Toegestane maximum massa voertuig"] = manual_df[
#     "Toegestane maximum massa voertuig"
# ].astype("UInt32")
# manual_df["Catalogusprijs"] = manual_df["Catalogusprijs"].astype("UInt32")
# manual_df["WAM verzekerd"] = manual_df["WAM verzekerd"].astype(
#     "category"
# )  # TODO: possibly boolean
# manual_df["Wacht op keuren"] = manual_df["Wacht op keuren"].astype("category")
# manual_df["Type gasinstallatie"] = manual_df["Type gasinstallatie"].astype("category")
# manual_df["Voertuigsoort"] = manual_df["Voertuigsoort"].astype("category")
# manual_df["Eerste kleur"] = manual_df["Eerste kleur"].astype("category")
# manual_df["Tweede kleur"] = manual_df["Tweede kleur"].astype("category")
# manual_df["Inrichting"] = manual_df["Inrichting"].astype("category")
# manual_df["Volgnummer wijziging EU typegoedkeuring"] = manual_df[
#     "Volgnummer wijziging EU typegoedkeuring"
# ].astype("UInt8")
# manual_df["Vervaldatum APK"] = pd.to_datetime(
#     manual_df["Vervaldatum APK"], format="%Y%m%d"
# )
# manual_df["Datum tenaamstelling"] = pd.to_datetime(
#     manual_df["Datum tenaamstelling"], format="%Y%m%d"
# )
# manual_df["Datum eerste toelating"] = pd.to_datetime(
#     manual_df["Datum eerste toelating"], format="%Y%m%d"
# )
# manual_df["Vervaldatum tachograaf"] = pd.to_datetime(
#     manual_df["Vervaldatum tachograaf"], format="%Y%m%d"
# )
#
# manual_df.to_csv(manual_name, index=False)

# profile = ProfileReport(manual_df, title="Manual")
# profile.to_file("manual_report.html", silent=False)

profile = ProfileReport(cast_df, title="Cast")
profile.to_file("cast_report.html", silent=False)
