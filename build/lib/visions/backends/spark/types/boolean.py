from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import BooleanType

from visions.types.boolean import Boolean


@Boolean.contains_op.register
def boolean_contains(sequence: DataFrame, state: dict) -> bool:
    if len(sequence.schema) != 1:
        return False

    dtype = sequence.schema[0].dataType
    return isinstance(dtype, BooleanType)
