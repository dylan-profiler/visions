from typing import TypeVar


backend = "pandas"
if backend == "pandas":
    import pandas as pd
    ColumnType = pd.Series
    FrameType = pd.DataFrame
elif backend == "spark":
    import pyspark
    ColumnType = pyspark.sql.column.Column
    FrameType = pyspark.sql.dataframe.DataFrame
else:
    raise ValueError

DataType = TypeVar("DataType", ColumnType, FrameType)
