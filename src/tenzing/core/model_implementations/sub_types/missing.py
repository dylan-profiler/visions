from tenzing.core.model_implementations.sub_type import subType


class missing(subType):
    @staticmethod
    def get_mask(series):
        return series.isna()

    @staticmethod
    def contains_op(series):
        return series.hasnans
