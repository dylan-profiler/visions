import numpy as np

from tenzing.core.model_implementations.sub_type import subType


class infinite(subType):
    @staticmethod
    def get_mask(series):
        return np.isinf(series)

    @staticmethod
    def contains_op(series):
        return np.isinf(series).any()

    @staticmethod
    def summarization_op(series):
        summary = {}
        mask = np.isinf(series)
        summary["inf_count"] = mask.values.sum()
        summary["perc_inf"] = (
            summary["inf_count"] / series.shape[0] if series.shape[0] > 0 else 0
        )
        return summary
