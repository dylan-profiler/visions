from pyspark.sql.column import Column
from pyspark.sql.types import BooleanType

from visions.types.boolean import Boolean


@Boolean.contains_op.register
def boolean_contains(sequence: Column, state: dict) -> bool:
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, BooleanType)
