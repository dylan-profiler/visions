from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import ArrayType, DateType, MapType, StringType, StructType

from visions.types.object import Object


@Object.contains_op.register
def object_contains(sequence: DataFrame, state: dict) -> bool:
    if len(sequence.schema) != 1:
        return False

    dtype = sequence.schema[0].dataType
    return isinstance(dtype, (StringType, DateType, ArrayType, MapType, StructType))
