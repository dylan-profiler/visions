from tenzing.core.model.model_relation import relation_conf
from tenzing.core.model.types import (
    tenzing_bool,
    tenzing_float,
    tenzing_object,
    tenzing_categorical,
    tenzing_ordinal,
    tenzing_datetime,
    tenzing_timedelta,
    tenzing_integer,
    tenzing_string,
    tenzing_url,
    tenzing_date,
    tenzing_time,
    tenzing_complex)
from tenzing.core.model.typeset import tenzingTypeset


# TODO: move to contrib
import pandas as pd


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_str(s):
    if s.str.len().max() == 1:
        unique_values = list(s[s.notna()].str.lower().unique())
        return "a" in unique_values and check_consecutive(list(map(ord, unique_values)))
    else:
        return False


def to_ordinal(series: pd.Series) -> pd.Series:
    return pd.Series(
        pd.Categorical(series, categories=sorted(series[series.notna()].unique()), ordered=True)
    )


def string_ordinal_contrib():
    return relation_conf(
        inferential=True,
        relationship=is_ordinal_str,
        transformer=to_ordinal
    )


class rdw_typeset(tenzingTypeset):
    """Typeset used in the RDW dataset"""

    def __init__(self):
        types = {
            tenzing_bool,
            tenzing_float,
            tenzing_object,
            tenzing_categorical,
            tenzing_ordinal,
            tenzing_datetime,
            tenzing_timedelta,
            tenzing_integer,
            tenzing_string,
            tenzing_url,
            tenzing_date,
            tenzing_time,
            tenzing_complex,
        }
        super().__init__(types, build=False)

        self.relations[tenzing_ordinal][tenzing_string] = string_ordinal_contrib()
        # self.relations[tenzing_bool][tenzing_string].map.append(
        #     {"Ja": True, "Nee": False}
        # )
        self._build_graph()
