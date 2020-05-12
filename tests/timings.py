import pandas as pd
from visions.utils.profiling import profile_type
from visions import Generic
from tests.series import get_series, get_contains_map, get_convert_map


def performance_report():
    series_dict = {s.name: s for s in get_series()}
    conv_map = get_contains_map()
    performance_list = []
    for type, series_names in conv_map.items():
        test_series = {name: series_dict[name] for name in series_names}
        performance_list.extend(profile_type(type, test_series))

    df = pd.DataFrame.from_records(performance_list)
    df["type"] = df["type"].astype(str)
    slow_df = df.groupby("type").min().reset_index()[["type", "series"]]
    slow_df.rename(columns={"series": "slowest test"}, inplace=True)

    df["normed run time"] = df["average run time"] / df["average run time"].min()
    df = df.groupby("type")["normed run time"].describe().sort_values("50%")
    df = pd.merge(df, slow_df, on="type", how="left")
    return df
