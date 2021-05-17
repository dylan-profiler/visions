from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import DecimalType, DoubleType, FloatType

from visions.types.float import Float


@Float.contains_op.register
def float_contains(sequence: DataFrame, state: dict) -> bool:
    if len(sequence.schema) != 1:
        return False

    dtype = sequence.schema[0].dataType
    return isinstance(dtype, (FloatType, DoubleType, DecimalType))
