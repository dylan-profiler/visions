from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import FloatType

from visions.types.float import Float


@Float.contains_op.register
def float_contains(sequence: DataFrame, state: dict) -> bool:
    assert len(sequence.schema) == 1
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, FloatType)
