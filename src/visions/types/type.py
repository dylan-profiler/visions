from abc import abstractmethod, ABCMeta
from types import FunctionType
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
    def evolve_type(
        cls,
        type_name: str,
        relations_generator: Optional[Callable] = None,
        replace: bool = False
    ):
        """Make a copy of the type with the relations replaced by the relations return by `relations_func`.

        Args:
            type_name: the new type suffix, the type name will be `type[type_name]`
            relations_func: a function returning all TypeRelations for the new type

        Returns:
            A new type
        """
        new_type = type(
                    "{name}[{type_name}]".format(name=cls.__name__, type_name=type_name),
                    (cls,),
                    {
                        "get_relations": classmethod(lambda _: NotImplemented),
                        "contains_op": cls.contains_op,
                    },
        )
        new_relations = list(relations_generator(new_type)) if relations_generator else []
        if replace:
            assert relations_generator is not None, "When calling evolve_type with `replace=True`, a `relations_generator` is required."
            relations_method = classmethod(lambda _: new_relations)
        else:
            old_relations = [attr.evolve(x, type=new_type) for x in cls.get_relations()]
            relations_method = classmethod(lambda _: old_relations + new_relations)
        new_type.get_relations = relations_method
        return new_type
