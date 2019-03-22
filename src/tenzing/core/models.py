from functools import singledispatch
from tenzing.utils import singleton
from abc import abstractmethod
import pandas as pd


def _is_true(*args, **kwargs):
    return True


def _real_values(self, series):
    return series.notna()


class model_relation:
    """
    Hub and spoke model - these are relationships of the form
    friend_model -> model of model_relation

    """
    def __init__(self, friend_model, relationship, transformer):
        self.friend_model = friend_model
        self.relationship = relationship
        self.transformer = transformer

    def is_relation(self, obj):
        return self.relationship(obj)

    def transform(self, obj):
        return self.transformer(obj)


class tenzing_typeset:
    def __init__(self, types):
        self.types = frozenset(types)

        self.relation_map = {typ: {} for typ in self.types}
        for typ in self.types:
            for friend_type, relation in typ.relations.items():
                self.relation_map[friend_type][typ] = relation


class optionMixin:
    is_option = True

    def cast(self, series):
        idx = series.notna()
        result = series.copy()
        result[idx] = self.cast_op(series[idx])
        return result

    def __contains__(self, series):
        idx = series.isna()
        notna_series = series[~idx].infer_objects() if idx.any() else series
        return self.contains_op(notna_series)


class relationMixin:
    def __init__(self):
        self.relations = {}

    def register_relation(self, relation):
        assert relation.friend_model not in self.relations, "Only one relationship permitted per type"
        self.relations[relation.friend_model] = relation


class tenzing_model(metaclass=singleton.Singleton):
    is_option = False
    relations = {}

    def cast(self, series):
        return self.cast_op(series)

    def __contains__(self, series):
        return self.contains_op(series)

    @abstractmethod
    def contains_op(self, series):
        pass

    @abstractmethod
    def cast_op(self, series):
        pass
