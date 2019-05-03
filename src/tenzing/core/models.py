from functools import singledispatch
from tenzing.utils import singleton
from abc import abstractmethod, abstractproperty, ABCMeta
import pandas as pd


class model_relation:
    """
    Hub and spoke model - these are relationships of the form
    friend_model -> model of model_relation

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
