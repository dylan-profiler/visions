import pandas as pd
import numpy as np
import big_o
from visions.utils.profiling import profile_type
from tests.series import get_series, get_contains_map


def big_o_tester(type):
    def inner(test_series):
        try:
            res = big_o.big_o(
                lambda x: x in type,
                lambda n: test_series[0:n],
                max_n=test_series.shape[0],
            )
            return res[0]
        except np.linalg.LinAlgError:
            return np.nan

    return inner


def performance_report(membership=True):
    series_dict = {s.name: s for s in get_series()}
    conv_map = get_contains_map()
    performance_list = []

    for type, series_names in conv_map.items():
        if membership:
            # True: "series in type"
            test_series = {name: series_dict[name] for name in series_names}
        else:
            # False: "series in type"
            test_series = {
                name: series_dict[name]
                for name in series_dict.keys()
                if name not in series_names
            }
        performance_list.extend(profile_type(type, test_series))

    df = pd.DataFrame.from_records(performance_list)

    df["type"] = df["type"].astype(str)
    aggs = ["min", "max"]
    agg_labels = ["worst", "best"]
    summary_cols = ["series", "big O"]
    agg_df = df.groupby("type").agg(aggs).reset_index()[["type"] + summary_cols]
    agg_df.columns = ["_".join(col).strip("_") for col in agg_df.columns]
    colrenames = {
        f"{name}_{agg}": f"{rename} {name}"
        for name in summary_cols
        for agg, rename in zip(aggs, agg_labels)
    }
    agg_df.rename(columns=colrenames, inplace=True)
    df["normed run time"] = df["average run time"] / df["average run time"].min()
    df = df.groupby("type")["normed run time"].describe().sort_values("50%")
    df = pd.merge(df, agg_df, on="type", how="left")
    return df
