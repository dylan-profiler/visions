from visions.core.model import TypeRelation


def string_to_categorical():
    # TODO: only when not any other string relation (either exclude others or have ordering and evaluate last)
    return TypeRelation(
        inferential=True, relationship=lambda s: s, transformer=lambda s: s
    )
