from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StringType

from visions.types.string import String


@String.contains_op.register
def string_contains(sequence: DataFrame, state: dict) -> bool:
    if len(sequence.schema) != 1:
        return False

    dtype = sequence.schema[0].dataType
    return isinstance(dtype, StringType)
