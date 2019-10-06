from tenzing.core.model.model_relation import relation_conf
from tenzing.utils.coercion import test_utils
import pandas as pd


def to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series)


# TODO: do only convert obvious dates (20191003000000)
def integer_to_datetime():
    return relation_conf(
        inferential=True,
        relationship=test_utils.coercion_test(lambda s: to_datetime(s.astype(str))),
        transformer=to_datetime,
    )
