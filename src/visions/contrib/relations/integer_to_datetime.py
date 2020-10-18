# import pandas as pd
#
# from visions.backends.pandas_be import test_utils
# from visions.relations import InferenceRelation
# from visions.relations.string_to_datetime import to_datetime_year_month_day
# from visions.types import Integer
#
#
# def to_datetime(series: pd.Series) -> pd.Series:
#     return pd.to_datetime(series)
#
#
# def _to_datetime(func) -> InferenceRelation:
#     return InferenceRelation(
#         relationship=test_utils.coercion_test(lambda s: func(s.astype(str))),
#         transformer=to_datetime,
#         related_type=Integer,
#     )
#
#
# # TODO: do only convert obvious dates (20191003000000)
# def integer_to_datetime(cls):
#     return _to_datetime(cls, to_datetime)
#
#
# def integer_to_datetime_year_month_day(cls) -> InferenceRelation:
#     return _to_datetime(cls, to_datetime_year_month_day)
