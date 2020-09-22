import pandas as pd


def get_geometry_series():
    from shapely import wkt

    series = [
        pd.Series(
            ["POINT (-92 42)", "POINT (-92 42.1)", "POINT (-92 42.2)"],
            name="geometry_string_series",
        ),
        pd.Series(
            [
                wkt.loads("POINT (-92 42)"),
                wkt.loads("POINT (-92 42.1)"),
                wkt.loads("POINT (-92 42.2)"),
            ],
            name="geometry_series",
        ),
        pd.Series(
            [
                wkt.loads("POINT (-92 42)"),
                wkt.loads("POINT (-92 42.1)"),
                wkt.loads("POINT (-92 42.2)"),
                None,
            ],
            name="geometry_series_missing",
        ),
    ]
    return series
