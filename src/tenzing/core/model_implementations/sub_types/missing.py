from tenzing.core.model_implementations.sub_type import subType


class missing(subType):
    @staticmethod
    def get_mask(series):
        return series.isna()

    @staticmethod
    def contains_op(series):
        return series.hasnans

    @staticmethod
    def summarization_op(series):
        mask = series.isna()
        summary = {}
        summary["na_count"] = mask.values.sum()
        summary["perc_na"] = (
            summary["na_count"] / series.shape[0] if series.shape[0] > 0 else 0
        )
        return summary
