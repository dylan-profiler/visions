from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import TimestampType

from visions.types.date_time import DateTime


@DateTime.contains_op.register
def datetime_contains(sequence: DataFrame, state: dict) -> bool:
    if len(sequence.schema) != 1:
        return False

    dtype = sequence.schema[0].dataType
    return isinstance(dtype, TimestampType)
