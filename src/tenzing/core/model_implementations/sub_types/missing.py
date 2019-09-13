from tenzing.core.model_implementations.sub_type import subType


class missing(subType):
    @staticmethod
    def get_mask(series):
        return series.isna()

    # @classmethod
    # def summarization_op(cls, series):
    #     print('option.summarization_op')
    #     idx = series.isna()
    #     summary = super().summarization_op(series[~idx])
    #
    #     summary["na_count"] = idx.values.sum()
    #     summary["perc_na"] = (
    #         summary["na_count"] / series.shape[0] if series.shape[0] > 0 else 0
    #     )
    #     return summary
