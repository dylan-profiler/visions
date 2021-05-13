from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import NumericType

from visions.types.numeric import Numeric


@Numeric.contains_op.register
def numeric_contains(sequence: DataFrame, state: dict) -> bool:
    assert len(sequence.schema) == 1
    dtype = sequence.schema[0].dataType
    return isinstance(dtype, NumericType)
