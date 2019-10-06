from tenzing.core.model.model_relation import relation_conf


def string_to_categorical():
    # TODO: only when not any other string relation (either exclude others or have ordering and evaluate last)
    return relation_conf(inferential=True, relationship=lambda s: s, transformer=lambda s: s)
