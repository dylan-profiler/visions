from abc import abstractmethod, ABCMeta
import pandas as pd


class meta_model(ABCMeta):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            from tenzing.core.model.types.tenzing_generic import tenzing_generic

            return cls == tenzing_generic
        return cls.contains_op(series)

    def __str__(cls) -> str:
        return f"{cls.__name__}"

    def __repr__(cls) -> str:
        return str(cls)


class tenzing_model(metaclass=meta_model):
    """Abstract implementation of a tenzing type.

    Provides a common API for building custom tenzing datatypes. These can optionally
    be augmented with mixins from :mod:`tenzing.core.mixins`

    Examples:
        >>> class tenzing_datetime(tenzing_model):
        >>>     def contains_op(self, series):
        >>>         return pdt.is_datetime64_dtype(series)
        >>>
        >>>     def cast_op(self, series):
        >>>         return pd.to_datetime(series)
        >>>
    """

    # # TODO: is this even used?
    # @classmethod
    # def __instancecheck__(mcs, instance) -> bool:
    #     print(mcs, instance.__class__)
    #     if instance.__class__ is mcs:
    #         return True
    #     else:
    #         return isinstance(instance.__class__, mcs)
    #

    @classmethod
    def cast(cls, series: pd.Series, operation=None):
        operation = operation if operation is not None else cls.cast_op
        return operation(series)

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def cast_op(cls, series: pd.Series) -> pd.Series:
        raise NotImplementedError
