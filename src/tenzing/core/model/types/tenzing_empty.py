# import pandas as pd
#
# from tenzing.core import tenzing_model
#
#
# class tenzing_empty(tenzing_model):
#     """**Empty series** implementation of :class:`tenzing.core.models.tenzing_model`.
#
#     Examples:
#         >>> x = pd.Series([], dtype=bool)
#         >>> x in tenzing_empty
#         True
#     """
#
#     @classmethod
#     def mask(cls, series: pd.Series) -> pd.Series:
#         # TODO
#         return series
#
#     @classmethod
#     def contains_op(cls, series: pd.Series) -> bool:
#         return series.empty
#
#     @classmethod
#     def cast_op(cls, series: pd.Series, operation=None) -> pd.Series:
#         return pd.Series([], name=series.name, dtype=series.dtype)
