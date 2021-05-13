from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import DateType

from visions.types.date import Date


@Date.contains_op.register
def date_contains(sequence: DataFrame, state: dict) -> bool:
    assert len(sequence.schema) == 1
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, DateType)
