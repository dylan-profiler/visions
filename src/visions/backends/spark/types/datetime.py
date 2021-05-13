from pyspark.sql.column import Column
from pyspark.sql.types import DateType

from visions.types.date_time import DateTime


@DateTime.contains_op.register
def datetime_contains(sequence: Column, state: dict) -> bool:
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, DateType)
