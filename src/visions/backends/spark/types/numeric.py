from pyspark.sql.column import Column
from pyspark.sql.types import NumericType

from visions.types.numeric import Numeric


@Numeric.contains_op.register
def numeric_contains(sequence: Column, state: dict) -> bool:
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, NumericType)
