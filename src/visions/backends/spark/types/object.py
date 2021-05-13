from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import DateType, StringType

from visions.types.object import Object


@Object.contains_op.register
def object_contains(sequence: DataFrame, state: dict) -> bool:
    assert len(sequence.schema) == 1
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, (StringType, DateType))
