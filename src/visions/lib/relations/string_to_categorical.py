from visions import visions_string, visions_categorical
from visions.core.model import TypeRelation


def string_to_categorical_distinct_count() -> TypeRelation:
    """Convert string to categorical when it has fewer than 50% unique values.

    Returns:
        relation
    """
    # TODO: only when not any other string relation (either exclude others or have ordering and evaluate last)
    return TypeRelation(
        inferential=True,
        relationship=lambda s: s.nunique() / len(s) < 0.5,
        transformer=lambda s: s.astype("category"),
        related_type=visions_string,
        type=visions_categorical,
    )
