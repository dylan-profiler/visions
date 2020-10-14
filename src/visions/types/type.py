from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional, Sequence, Type, Union, cast

from multimethod import multimethod

from visions.relations import TypeRelation, IdentityRelation

_DEFAULT = object()


class RelationsIterManager:
    """Class to enable to treat relations as dict"""

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

    def __iter__(self):
        yield from self.values


class VisionsBaseTypeMeta(ABCMeta):
    _relations: Optional[RelationsIterManager] = None

    def __contains__(cls, sequence: Sequence) -> bool:
        return cls.contains_op(sequence, dict())

    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @staticmethod
    def contains_op(item: Any, state: dict) -> bool:
        raise NotImplementedError

    @property
    def relations(cls) -> RelationsIterManager:
        if cls._relations is None:
            cls._relations = RelationsIterManager(cls.get_relations())
        return cls._relations

    def __add__(cls, other):
        from visions.types import Generic
        from visions.typesets import VisionsTypeset

        if not any(issubclass(x, Generic) for x in [cls, other]):
            return VisionsTypeset({Generic, cls, other})
        return VisionsTypeset({cls, other})

    def __str__(cls) -> str:
        return str(cls.__name__)

    def __repr__(cls) -> str:
        return str(cls)


class VisionsBaseType(metaclass=VisionsBaseTypeMeta):
    """Abstract implementation of a vision type.

    Provides a common API for building custom visions data types.
    """

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_relations(cls) -> Sequence[TypeRelation]:
        raise NotImplementedError

    @classmethod
    def register_transformer(
        cls, relation: "Type[VisionsBaseType]", dispatch_type: Any
    ):
        relation_transformer = cls.relations[relation].transformer
        return cast(Any, relation_transformer).register(dispatch_type, dict)

    @classmethod
    def register_relationship(
        cls, relation: "Type[VisionsBaseType]", dispatch_type: Any
    ):
        relation_relationship = cls.relations[relation].relationship
        return cast(Any, relation_relationship).register(dispatch_type, dict)

    @staticmethod
    @multimethod
    @abstractmethod
    def contains_op(sequence: Any, state: Any) -> bool:
        raise NotImplementedError
