from abc import abstractmethod, ABCMeta
from types import FunctionType
from typing import Sequence, Callable, Type

import pandas as pd

from visions.relations import TypeRelation


class VisionsBaseTypeMeta(ABCMeta):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            from visions.types import Generic

            return cls == Generic
        return cls.contains_op(series)  # type: ignore

    @property
    def relations(cls):
        if clas._relations is None:
            cls._relations = cls.get_relations()
        return cls._relations

    def __str__(cls) -> str:
        return str(cls.__name__)

    def __repr__(cls) -> str:
        return str(cls)


class VisionsBaseType(metaclass=VisionsBaseTypeMeta):
    """Abstract implementation of a vision type.

    Provides a common API for building custom visions data types.
    """
    _relations : Optional[Sequence] = None

    def __init__(self):
        raise ValueError('Types cannot be initialized')

    @classmethod
    @abstractmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

    @property
    def relations(self):
        return type(self).relations

    @classmethod
    def evolve_extend_relations(
        cls,
        type_name: str,
        relations_func: Callable[[Type[VisionsBaseTypeMeta]], TypeRelation],
    ):
        """Make a copy of the type with the relations extended by the TypeRelation returned by `relations_func`.

        Args:
            type_name: the new type suffix, the type name will be `type[type_name]`
            relations_func: a function returning the additional TypeRelations for the new type

        Returns:
            A new type
        """
        f = cls.get_relations
        default_relations = FunctionType(
            f.__code__, f.__globals__, f.__name__, f.__defaults__, f.__closure__
        )
        return cls.evolve_replace_relations(
            type_name, lambda c: default_relations(c) + [relations_func(c)]
        )

    @classmethod
    def evolve_relations(
        cls,
        type_name: str,
        new_relations: Sequence[TypeRelation],
    ):
        """Make a copy of the type with the relations replaced by the relations return by `relations_func`.

        Args:
            type_name: the new type suffix, the type name will be `type[type_name]`
            relations_func: a function returning all TypeRelations for the new type

        Returns:
            A new type
        """
        def get_new_relations(c)
        old_relations = [attr.evolve(relation, type=type_name) for relation in cls.relations]
        return old_relations + list(new_relations)
