from visions.core.model.relations import InferenceRelation
from visions.core.implementations.types.visions_ordinal import to_ordinal


def check_consecutive(l) -> bool:
    return sorted(l) == list(range(min(l), max(l) + 1))


def is_ordinal_int(s) -> bool:
    unique_values = list(s.unique())
    return (
        check_consecutive(unique_values)
        and 2 < len(unique_values) < 10
        and 1 in unique_values
    )


def integer_to_ordinal() -> InferenceRelation:
    from visions.core.implementations.types import visions_ordinal, visions_integer

    return InferenceRelation(
        visions_ordinal,
        visions_integer,
        relationship=is_ordinal_int,
        transformer=to_ordinal,
    )
