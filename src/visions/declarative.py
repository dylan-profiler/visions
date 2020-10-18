from typing import Any, Callable, List, Optional, Type, TypeVar, Union

from visions.relations import IdentityRelation, InferenceRelation
from visions.types.type import VisionsBaseType

T = TypeVar("T")


def create_type(
    name: str,
    contains: Callable[[Any, dict], bool],
    identity: Optional[Union[Type[VisionsBaseType], List[dict], dict]] = None,
    inference: Optional[Union[List[dict], dict]] = None,
):
    def get_relations(cls):
        relations = []
        if identity is not None:
            if isinstance(identity, list):
                relations += [IdentityRelation(cls, **params) for params in identity]
            elif isinstance(identity, dict):
                relations += [IdentityRelation(cls, **identity)]
            elif issubclass(identity, VisionsBaseType):
                relations += [IdentityRelation(cls, related_type=identity)]
            else:
                raise TypeError(
                    "identity should be a list, a dict of params or related_type."
                )

        if inference is not None:
            if isinstance(inference, dict):
                relations += [InferenceRelation(cls, **inference)]
            elif isinstance(inference, list):
                relations += [InferenceRelation(cls, **params) for params in inference]
            else:
                raise TypeError("identity should be a list or a dict of params.")

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
