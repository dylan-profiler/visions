import pytest
from visions.typesets import StandardSet
from visions.types import Boolean, Float, Object, Complex, Categorical, DateTime, TimeDelta, String


@pytest.fixture()
def spark():
    from pyspark.sql import SparkSession
    return SparkSession.builder.appName("Test Spark Backend").getOrCreate()


def test_spark_inference(spark):
    from pyspark.sql.types import StructField, StringType, IntegerType, StructType

    schema = StructType(fields=[StructField('age', IntegerType(), True), StructField('name', StringType(), True)])
    df = spark.createDataFrame([{"name": "John", "age": 24}], schema=schema)

    abc = StandardSet() - Boolean - Float - Object - Complex - Categorical - DateTime - TimeDelta - String
    print(abc.infer_type(df['name']))