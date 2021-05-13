from pyspark.sql.dataframe import DataFrame

from visions.types.categorical import Categorical


@Categorical.contains_op.register
def categorical_contains(sequence: DataFrame, state: dict) -> bool:
    assert len(sequence.schema) == 1
    return False
