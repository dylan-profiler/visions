from abc import abstractmethod
import pandas as pd
import numpy as np
from tenzing.core.reuse.base_summary import base_summary


class model_relation:
    """Relationship encoder between implementations of :class:`tenzing.core.models.tenzing_model`

    Defines a one to one relationship between two tenzing_model implementations,
    A and B, with respect to an underlying data series. In order to define a relationship we need
    two methods:

        - **is_relationship**, determines whether a series of type B can be alternatively represented as type A.
        - **transform**, provides a mechanism to convert the series from B -> A.

    For example, the series `pd.Series([1.0, 2.0, 3.0])` is encoded as a sequence of
    floats but in reality they are all integers.

    >>> x = pd.Series([1.0, 2.0, 3.0])
    >>> relation = model_relation(tenzing_integer, tenzing_float)
    >>> relation.is_relation(x)
    True

    >>> relation.transform(x)
    pd.Series([1, 2, 3])

    Parameters
    ----------
    model : tenzing_type
        The type this relation will transform a series into.

    friend_model : tenzing_type
        The type this relation will transform a series from.

    relationship : func
        A method to determine if a series of friend_model type can be converted to type model.

    transformer : func
        A method to convert a series from type friend_model to type model.

    """

    def __init__(self, model, friend_model, relationship=None, transformer=None):
        self.model = model
        self.friend_model = friend_model
        self.edge = (self.friend_model, self.model)
        # TODO: should not be optional
        self.relationship = relationship if relationship else self.model.__contains__
        self.transformer = transformer

    def is_relation(self, obj):
        return self.relationship(self.friend_model.get_series(obj))

    def transform(self, obj):
        return self.model.cast(obj, self.transformer)

    def __repr__(self):
        return f"({self.friend_model} -> {self.model})"


class meta_model(type):
    def __contains__(cls, series):
        return cls.contains_op(series)

    def __repr__(cls):
        return cls.__name__

    # TODO: raise exception on instantiation
    #     raise Exception("Cannot instantiate a type!")

    # TODO: automatic static ?
    # https://stackoverflow.com/questions/31953113/purely-static-classes-in-python-use-metaclass-class-decorator-or-something-e


class tenzing_model(metaclass=meta_model):
    """Abstract implementation of a tenzing type.

    Provides a common API for building custom tenzing datatypes. These can optionally
    be augmented with mixins from :mod:`tenzing.core.mixins`

    i.e.

    >>> class tenzing_datetime(tenzing_model):
    >>>     def contains_op(self, series):
    >>>         return pdt.is_datetime64_dtype(series)
    >>>
    >>>     def cast_op(self, series):
    >>>         return pd.to_datetime(series)
    >>>
    >>>     def summarization_op(self, series):
    >>>         summary = super().summarization_op(series)
    >>>         aggregates = ['min', 'max']
    >>>         summary.update(series.agg(aggregates).to_dict())
    >>>
    >>>         summary['range'] = summary['max'] - summary['min']
    >>>         return summary
    """

    _relations = {}

    @staticmethod
    def get_series_mask(series):
        return np.ones_like(series, dtype=bool)

    @classmethod
    def get_series(cls, series):
        return series

    @classmethod
    def __instancecheck__(mcs, instance):
        if instance.__class__ is mcs:
            return True
        else:
            return isinstance(instance.__class__, mcs)

    @classmethod
    def get_relations(cls):
        # TODO: move to __new__ or so?
        if cls.__name__ not in cls._relations:
            cls._relations[cls.__name__] = {}

        return cls._relations[cls.__name__]

    @classmethod
    def register_relation(cls, relation):
        if cls.__name__ not in cls._relations:
            cls._relations[cls.__name__] = {}

        assert (
            relation.friend_model not in cls._relations[cls.__name__]
        ), "Only one relationship permitted per type"
        cls._relations[cls.__name__][relation.friend_model] = relation

    @classmethod
    def cast(cls, series, operation=None):
        operation = operation if operation is not None else cls.cast_op
        return operation(series)

    @classmethod
    @base_summary
    def summarize(cls, series):
        print('tenzing_model.summarize')
        return cls.summarization_op(series)

    @classmethod
    @abstractmethod
    def contains_op(cls, series):
        pass

    @classmethod
    @abstractmethod
    def cast_op(cls, series):
        pass

    @classmethod
    @abstractmethod
    def summarization_op(cls, series):
        print('tenzing_model.summarization_op')
        return {}
