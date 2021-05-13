from pyspark.sql.column import Column

from visions.types.categorical import Categorical


@Categorical.contains_op.register
def categorical_contains(sequence: Column, state: dict) -> bool:
    return False
