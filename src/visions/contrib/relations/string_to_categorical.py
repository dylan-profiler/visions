# from visions import String
# from visions.relations.relations import InferenceRelation
#
#
# def string_to_categorical_distinct_count() -> InferenceRelation:
#     """Convert string to categorical when it has fewer than 50% unique values.
#
#     Returns:
#         relation
#     """
#     # TODO: only when not any other string relation (either exclude others or have ordering and evaluate last)
#     return InferenceRelation(
#         relationship=lambda s, state: s.nunique() / len(s) < 0.5,
#         transformer=lambda s: s.astype("category"),
#         related_type=String,
#     )
