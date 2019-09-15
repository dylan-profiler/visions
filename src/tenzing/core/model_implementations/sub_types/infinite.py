import numpy as np

from tenzing.core.model_implementations.sub_type import subType


class infinite(subType):
    @staticmethod
    def get_mask(series):
        return (~np.isfinite(series)) & series.notnull()

    @staticmethod
    def contains_op(series):
        return ((~np.isfinite(series)) & series.notnull()).any()
