from pyspark.sql.column import Column
from pyspark.sql.types import StringType

from visions.types.string import String


@String.contains_op.register
def string_contains(sequence: Column, state: dict) -> bool:
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, StringType)
