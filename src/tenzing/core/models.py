from functools import singledispatch
from tenzing.utils import singleton
from abc import abstractmethod, abstractproperty, ABCMeta
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
    def __init__(self, model, friend_model, relationship=None, transformer=None):
        self.model = model
        self.friend_model = friend_model
        self.relationship = relationship if relationship else self.model.__contains__
        self.transformer = transformer if transformer else self.model.cast

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


class tenzing(tenzing_typeset):
    def __init__(self, types):
        self.column_type_map = {}
        super().__init__(types)

    def prep(self, df):
        self.column_type_map = {col: self._get_column_type(df[col]) for col in df.columns}
        return self

    def summarize(self, df):
        summary = {col: self.column_type_map[col].summarize(df[col]) for col in df.columns}
        return summary

    def _get_column_type(self, series):
        # walk the relation_map to determine which is most uniquely specified
        candidates = [tenzing_type for tenzing_type in self.types if series in tenzing_type]
        if len(candidates) > 1:
            print("You forgot to implement handling for multiple matches. Go fix that retard")
        return candidates[0]


class tenzing_model(metaclass=singleton.Singleton):
    is_option = False

    def __init__(self):
        self.relations = {}

    def register_relation(self, relation):
        assert relation.friend_model not in self.relations, "Only one relationship permitted per type"
        self.relations[relation.friend_model] = relation

    def cast(self, series):
        return self.cast_op(series)

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
