import pandas as pd

from tests.typesets.test_complete_set import convert_map
from visions.test.series import get_series
from visions.utils.profiling import (
    profile_relation_is_relation,
    profile_relation_transform,
    profile_type,
)


def performance_report(membership=True):
    series_dict = {s.name: s for s in get_series()}
    conv_map = convert_map
    performance_list = []

    for type, series_names in conv_map.items():
        if membership:
            # True: "series in type"
            test_series = {name: series_dict[name] for name in series_names}
        else:
            # False: "series in type"
            test_series = {
                s.name: s for s in series_dict.values() if s.name not in series_names
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


def get_relation(to_type, from_type):
    return to_type.relations[from_type]


def relations_is_relation_test():
    relation_tests = {
        get_relation(*conversions[0:2]): conversions[2] for conversions in convert_map
    }

    series_dict = {s.name: s for s in get_series()}
    performance_list = []
    for relation, names in relation_tests.items():
        test_series = {name: series_dict[name] for name in names}
        performance_list.extend(profile_relation_is_relation(relation, test_series))
    df = pd.DataFrame.from_records(performance_list)
    grouper = "relation"
    df[grouper] = df[grouper].astype(str)
    aggs = ["min", "max"]
    agg_labels = ["worst", "best"]
    summary_cols = ["series", "big O"]
    agg_df = df.groupby(grouper).agg(aggs).reset_index()[[grouper] + summary_cols]
    agg_df.columns = ["_".join(col).strip("_") for col in agg_df.columns]
    colrenames = {
        f"{name}_{agg}": f"{rename} {name}"
        for name in summary_cols
        for agg, rename in zip(aggs, agg_labels)
    }
    agg_df.rename(columns=colrenames, inplace=True)
    df["normed run time"] = df["average run time"] / df["average run time"].min()
    df = df.groupby(grouper)["normed run time"].describe().sort_values("50%")
    df = pd.merge(df, agg_df, on=grouper, how="left")
    return df


def relations_transform_test():
    relation_tests = {
        get_relation(*conversions[0:2]): conversions[2] for conversions in convert_map
    }

    series_dict = {s.name: s for s in get_series()}
    performance_list = []
    for relation, names in relation_tests.items():
        test_series = {name: series_dict[name] for name in names}
        performance_list.extend(profile_relation_transform(relation, test_series))
    df = pd.DataFrame.from_records(performance_list)
    grouper = "relation"
    df[grouper] = df[grouper].astype(str)
    aggs = ["min", "max"]
    agg_labels = ["worst", "best"]
    summary_cols = ["series", "big O"]
    agg_df = df.groupby(grouper).agg(aggs).reset_index()[[grouper] + summary_cols]
    agg_df.columns = ["_".join(col).strip("_") for col in agg_df.columns]
    colrenames = {
        f"{name}_{agg}": f"{rename} {name}"
        for name in summary_cols
        for agg, rename in zip(aggs, agg_labels)
    }
    agg_df.rename(columns=colrenames, inplace=True)
    df["normed run time"] = df["average run time"] / df["average run time"].min()
    df = df.groupby(grouper)["normed run time"].describe().sort_values("50%")
    df = pd.merge(df, agg_df, on=grouper, how="left")
    return df
