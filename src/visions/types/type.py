from abc import abstractmethod, ABCMeta
from typing import Sequence, Callable, Type

import pandas as pd

from visions.relations import TypeRelation


class VisionsBaseTypeMeta(ABCMeta):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            from visions.types import Generic

            return cls == Generic
        return cls.contains_op(series)  # type: ignore

    def __str__(cls) -> str:
        return str(cls.__name__)

    def __repr__(cls) -> str:
        return str(cls)


class VisionsBaseType(metaclass=VisionsBaseTypeMeta):
    """Abstract implementation of a vision type.

    Provides a common API for building custom visions data types.
    """

    @classmethod
    @abstractmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

    @classmethod
    def evolve_extend_relations(
        cls,
        type_name: str,
        relations_func: Callable[[Type[VisionsBaseTypeMeta]], TypeRelation],
    ):
        """Make a copy of the type with the relations extended by the TypeRelation returned by `relations_func`.

        Notes:
            This function utilizes the importlib to dynamically import the `_get_relations` function that
            specifies the default relations of a type. We plan on updating the structure to allow for a
            more robust implementation for this functionality.

        Args:
            type_name: the new type suffix, the type name will be `type[type_name]`
            relations_func: a function returning the additional TypeRelations for the new type

        Returns:
            A new type
        """
        import importlib
        import re

        pattern = re.compile(r"(?<!^)(?=[A-Z])")
        snake = pattern.sub("_", str(cls)).lower()
        type_module = importlib.import_module("visions.types." + snake)
        default_relations = type_module._get_relations
        return cls.evolve_replace_relations(
            type_name, lambda c: default_relations(c) + [relations_func(c)]
        )

    @classmethod
    def evolve_replace_relations(
        cls,
        type_name: str,
        relations_func: Callable[[Type[VisionsBaseTypeMeta]], Sequence[TypeRelation]],
    ):
        """Make a copy of the type with the relations replaced by the relations return by `relations_func`.

        Args:
            type_name: the new type suffix, the type name will be `type[type_name]`
            relations_func: a function returning all TypeRelations for the new type

        Returns:
            A new type
        """
        return type(
            "{name}[{type_name}]".format(name=cls.__name__, type_name=type_name),
            (cls,),
            {
                "get_relations": classmethod(relations_func),
                "contains_op": cls.contains_op,
            },
        )
