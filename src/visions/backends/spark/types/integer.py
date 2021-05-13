from pyspark.sql.column import Column
from pyspark.sql.types import IntegerType

from visions.types.integer import Integer


@Integer.contains_op.register
def integer_contains(sequence: Column, state: dict) -> bool:
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, IntegerType)
