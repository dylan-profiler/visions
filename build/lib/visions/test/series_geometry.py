from typing import Dict

import pandas as pd


def get_geometry_series() -> Dict[str, pd.Series]:
    from shapely import wkt

    series = {
        "geometry_string_series": pd.Series(
            ["POINT (-92 42)", "POINT (-92 42.1)", "POINT (-92 42.2)"],
        ),
        "geometry_series": pd.Series(
            [
                wkt.loads("POINT (-92 42)"),
                wkt.loads("POINT (-92 42.1)"),
                wkt.loads("POINT (-92 42.2)"),
            ],
        ),
        "geometry_series_missing": pd.Series(
            [
                wkt.loads("POINT (-92 42)"),
                wkt.loads("POINT (-92 42.1)"),
                wkt.loads("POINT (-92 42.2)"),
                None,
            ],
        ),
    }
    return series
