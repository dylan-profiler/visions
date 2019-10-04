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

    Provides a common API for building custom tenzing datatypes.
    """

    # _relations = {}
    #
    # # TODO: is this even used?
    # @classmethod
    # def __instancecheck__(mcs, instance) -> bool:
    #     print(mcs, instance.__class__)
    #     if instance.__class__ is mcs:
    #         return True
    #     else:
    #         return isinstance(instance.__class__, mcs)

    # @classmethod
    # def get_relations(cls) -> dict:
    #     # TODO: move to __new__ or so?
    #     if cls.__name__ not in cls._relations:
    #         cls._relations[cls.__name__] = {}
    #
    #     return cls._relations[cls.__name__]

    # @classmethod
    # def register_relation(cls, relation) -> None:
    #     if cls.__name__ not in cls._relations:
    #         cls._relations[cls.__name__] = {}
    #
    #     assert (
    #         relation.friend_model not in cls._relations[cls.__name__]
    #     ), "Only one relationship permitted per type"
    #     cls._relations[cls.__name__][relation.friend_model] = relation

    @classmethod
    def cast(cls, series: pd.Series, operation=None):
        operation = operation if operation is not None else cls.cast_op
        return operation(series)

    @classmethod
    @abstractmethod
    def get_relations(cls) -> dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def cast_op(cls, series: pd.Series) -> pd.Series:
        raise NotImplementedError
