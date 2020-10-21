from typing import Any, Callable, List, Optional, Sequence, Type, TypeVar, Union

from visions.relations import IdentityRelation, InferenceRelation
from visions.types.type import VisionsBaseType

T = TypeVar("T")


def process_relation(items: Union[dict, Type[VisionsBaseType]]) -> IdentityRelation:
    if isinstance(items, dict):
        return IdentityRelation(**items)
    elif issubclass(items, VisionsBaseType):
        return IdentityRelation(related_type=items)
    else:
        raise TypeError("identity should be a list, a dict of params or related_type.")


def create_type(
    name: str,
    contains: Callable[[Any, dict], bool],
    identity: Optional[
        Union[Type[VisionsBaseType], List[Union[dict, Type[VisionsBaseType]]], dict]
    ] = None,
    inference: Optional[Union[List[dict], dict]] = None,
):
    def get_relations():
        if isinstance(identity, Sequence):
            relations = [process_relation(item) for item in identity]
        else:
            relations = [] if identity is None else [process_relation(identity)]

        if inference is not None:
            if isinstance(inference, dict):
                relations += [InferenceRelation(**inference)]
            elif isinstance(inference, list):
                relations += [InferenceRelation(**params) for params in inference]
            else:
                raise TypeError("inference should be a list or a dict of params.")

        return relations

    def contains_op(series, state):
        return contains(series, state)

    return type(
        name,
        (VisionsBaseType,),
        {
            "get_relations": staticmethod(get_relations),
            "contains_op": staticmethod(contains_op),
        },
    )
