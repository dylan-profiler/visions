from typing import Any, Callable, List, Optional, Type, TypeVar, Union, Sequence, List

from visions.relations import IdentityRelation, InferenceRelation
from visions.types.type import VisionsBaseType

T = TypeVar("T")


def process_relation(
    cls, items: Optional[Union[Sequence, dict, Type[VisionsBaseType]]]
) -> IdentityRelation:
    if isinstance(items, dict):
        return IdentityRelation(cls, **items)
    elif issubclass(items, VisionsBaseType):
        return IdentityRelation(cls, related_type=items)
    else:
        raise TypeError("identity should be a list, a dict of params or related_type.")


def create_type(
    name: str,
    contains: Callable[[Any, dict], bool],
    identity: Optional[Union[Type[VisionsBaseType], List[Union[dict, Type[VisionsBaseType]]], dict]] = None,
    inference: Optional[Union[List[dict], dict]] = None,
):
    def get_relations(cls):
        if isinstance(identity, Sequence):
            relation = [process_relation(item) for item in identity]
        else:
            relation = [] if identity is None else process_relation(identity)

        if inference is not None:
            if isinstance(inference, dict):
                relations += [InferenceRelation(cls, **inference)]
            elif isinstance(inference, list):
                relations += [InferenceRelation(cls, **params) for params in inference]
            else:
                raise TypeError("inference should be a list or a dict of params.")

        return relations

    def contains_op(series, state):
        return contains(series, state)

    return type(
        name,
        (VisionsBaseType,),
        {
            "get_relations": classmethod(get_relations),
            "contains_op": staticmethod(contains_op),
        },
    )
