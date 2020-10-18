from typing import Any, Callable, List, Optional, Type, TypeVar

from visions import VisionsBaseType
from visions.relations import IdentityRelation, InferenceRelation

T = TypeVar("T")


def create_type(
    name: str,
    identity: Type[VisionsBaseType],
    contains: Callable[[Any, dict], bool],
    inference: Optional[List[dict]] = None,
    transformer: Optional[Callable[[T, dict], T]] = None,
):
    def get_relations(cls):
        params = {"related_type": identity}
        if transformer is not None:
            params["transformer"] = transformer

        relations = [IdentityRelation(cls, **params)]
        if inference is not None:
            relations += [InferenceRelation(cls, **params) for params in inference]

        return relations

    def contains_op(cls, series, state):
        return contains(series, state)

    return type(
        name,
        (VisionsBaseType,),
        {
            "get_relations": classmethod(get_relations),
            "contains_op": classmethod(contains_op),
        },
    )
