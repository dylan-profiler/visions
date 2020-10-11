from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Dict, Optional, Sequence, Type, Union

import attr
import pandas as pd

from visions.relations import TypeRelation

_DEFAULT = object()


class RelationsIterManager:
    def __init__(self, relations: Sequence[TypeRelation]):
        self._keys: Dict["Type[VisionsBaseType]", int] = {
            item.related_type: i for i, item in enumerate(relations)
        }
        self.values = tuple(relations)

    def __getitem__(self, index: Union["Type[VisionsBaseType]", int]) -> TypeRelation:
        idx = index if isinstance(index, int) else self._keys[index]
        return self.values[idx]

    def get(
        self, index: Union["Type[VisionsBaseType]", int], default: Any = _DEFAULT
    ) -> Union[TypeRelation, Any]:
        try:
            return self[index]
        except (IndexError, KeyError) as err:
            if default is _DEFAULT:
                raise err
            else:
                return default


class VisionsBaseTypeMeta(ABCMeta):
    def __contains__(cls, series: pd.Series, state: dict = {}) -> bool:
        return cls.contains_op(series, state)  # type: ignore

    @property
    def relations(cls) -> RelationsIterManager:
        if cls._relations is None:  # type: ignore
            cls._relations = RelationsIterManager(cls.get_relations())  # type: ignore
        return cls._relations

    def __add__(cls, other):
        from visions.types import Generic
        from visions.typesets import VisionsTypeset

        if not any(issubclass(x, Generic) for x in [cls, other]):
            return VisionsTypeset([Generic, cls, other])
        return VisionsTypeset([cls, other])

    def __str__(cls) -> str:
        return str(cls.__name__)

    def __repr__(cls) -> str:
        return str(cls)


class VisionsBaseType(metaclass=VisionsBaseTypeMeta):
    """Abstract implementation of a vision type.

    Provides a common API for building custom visions data types.
    """

    _relations: Optional[Sequence[TypeRelation]] = None

    def __init__(self):
        raise ValueError("Types cannot be initialized")

    @classmethod
    @abstractmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def contains_op(cls, series: pd.Series, state: dict) -> bool:
        raise NotImplementedError

    @classmethod
    def evolve_type(
        cls,
        type_name: str,
        relations_generator: Optional[
            Callable[[Type[VisionsBaseTypeMeta]], Sequence[TypeRelation]]
        ] = None,
        replace: bool = False,
    ) -> "Type[VisionsBaseType]":
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

        name = cls.__name__
        new_type = type(
            f"{name}[{type_name}]",
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
                attr.evolve(relation, type=new_type) for relation in cls.relations
            ]
            relations = old_relations + new_relations

        return new_type
