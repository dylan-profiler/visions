from pyspark.sql.column import Column
from pyspark.sql.types import FloatType

from visions.types.float import Float


@Float.contains_op.register
def float_contains(sequence: Column, state: dict) -> bool:
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, FloatType)
