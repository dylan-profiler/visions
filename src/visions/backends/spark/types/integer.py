from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import ByteType, IntegerType, LongType, ShortType

from visions.types.integer import Integer


@Integer.contains_op.register
def integer_contains(sequence: DataFrame, state: dict) -> bool:
    if len(sequence.schema) != 1:
        return False

    dtype = sequence.schema[0].dataType
    return isinstance(dtype, (ByteType, ShortType, IntegerType, LongType))
