from abc import abstractmethod, ABCMeta
from typing import Sequence, Callable, Type, Optional

import attr
import pandas as pd

from visions.relations import TypeRelation


class VisionsBaseTypeMeta(ABCMeta):
    def __contains__(cls, series: pd.Series) -> bool:
        if series.empty:
            from visions.types import Generic

            return cls == Generic
        return cls.contains_op(series)  # type: ignore

    @property
    def relations(cls) -> Optional[Sequence[TypeRelation]]:
        if cls._relations is None:
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

    _relations = None

    def __init__(self):
        raise ValueError("Types cannot be initialized")

    @classmethod
    @abstractmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series) -> bool:
        raise NotImplementedError

    @classmethod
    def evolve_type(
        cls,
        type_name: str,
        relations_generator: Optional[
            Callable[[Type[VisionsBaseTypeMeta]], Sequence[TypeRelation]]
        ] = None,
        replace: bool = False,
    ):
        """Make a copy of the type

        Args:
            type_name: the new type suffix, the type name will be `type[type_name]`
            relations_generator: a function returning all TypeRelations for the new type
            replace: if True, do not include the existing relations

        Returns:
            A new type
        """

        def get_new_relations(cls) -> Sequence[TypeRelation]:
            return relations

        new_type = type(
            "{name}[{type_name}]".format(name=cls.__name__, type_name=type_name),
            (cls,),
            {
                "get_relations": classmethod(get_new_relations),
                "contains_op": cls.contains_op,
            },
        )
        new_relations = (
            list(relations_generator(new_type)) if relations_generator else []
        )
        if replace:
            assert (
                relations_generator is not None
            ), "When calling evolve_type with `replace=True`, a `relations_generator` is required."
            relations = new_relations
        else:
            old_relations = [
                attr.evolve(relation, type=new_type) for relation in cls.get_relations()
            ]
            relations = old_relations + new_relations

        return new_type
