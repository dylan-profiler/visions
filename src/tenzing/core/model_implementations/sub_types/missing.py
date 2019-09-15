from tenzing.core.model_implementations.sub_type import subType


class missing(subType):
    @staticmethod
    def get_mask(series):
        return series.isna()

    @staticmethod
    def contains_op(series):
        # TODO: all series should be nans
        return series.hasnans
