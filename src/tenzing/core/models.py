from functools import singledispatch
from tenzing.utils import singleton
from abc import abstractmethod, abstractproperty, ABCMeta
import pandas as pd


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
        self.relationship = relationship if relationship else self.model.__contains__
        self.transformer = transformer

    def is_relation(self, obj):
        return self.relationship(self.friend_model.get_series(obj))

    def transform(self, obj):
        return self.model.cast(obj, self.transformer)

    def __repr__(self):
        return f'({self.friend_model} -> {self.model})'


class tenzing_model(metaclass=singleton.Singleton):
    """Abstract implementation of a tenzing type.

    Provides a common API for building custom tenzing datatypes. These can optionally
    be augmented with mixins from :mod:`tenzing.core.mixins`

    i.e.

    >>> @singleton.singleton_object
    >>> class tenzing_timestamp(tenzing_model):
    >>>     def contains_op(self, series):
    >>>         return pdt.is_datetime64_dtype(series)
    >>>
    >>>     def cast_op(self, series):
    >>>         return pd.to_datetime(series)
    >>>
    >>>     def summarization_op(self, series):
    >>>         aggregates = ['nunique', 'min', 'max']
    >>>         summary = series.agg(aggregates).to_dict()
    >>>
    >>>         summary['n_records'] = series.shape[0]
    >>>         summary['perc_unique'] = summary['nunique'] / summary['n_records']
    >>>
    >>>         summary['range'] = summary['max'] - summary['min']
    >>>         return summary
    """

    is_option = False

    def __init__(self):
        self.relations = {}

    def get_series(self, series):
        return series

    def register_relation(self, relation):
        assert relation.friend_model not in self.relations, "Only one relationship permitted per type"
        self.relations[relation.friend_model] = relation

    def cast(self, series, operation=None):
        operation = operation if operation is not None else self.cast_op
        return operation(series)

    def summarize(self, series):
        return self.summarization_op(series)

    def __contains__(self, series):
        return self.contains_op(series)

    @abstractmethod
    def contains_op(self, series):
        pass

    @abstractmethod
    def cast_op(self, series):
        pass

    @abstractmethod
    def summarization_op(self, series):
        pass
