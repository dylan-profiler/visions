from tenzing.core.model.types.tenzing_object import tenzing_object


class tenzing_string(tenzing_object):
    """**String** implementation of :class:`tenzing.core.models.tenzing_model`.

    >>> x = pd.Series(['a', 'b', np.nan])
    >>> x in tenzing_string
    True
    """

    @classmethod
    def contains_op(cls, series):
        if not super().contains_op(series):
            return False

        return series.copy().apply(lambda x: type(x) == str).all()

    @classmethod
    def cast_op(cls, series, operation=None):
        return series.astype(str)
