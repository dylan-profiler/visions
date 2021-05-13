from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import IntegerType

from visions.types.integer import Integer


@Integer.contains_op.register
def integer_contains(sequence: DataFrame, state: dict) -> bool:
    assert len(sequence.schema) == 1
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, IntegerType)
