import sys

import pytest


@pytest.mark.spark_test
def test_import_spark_session(spark_session):
    """
    Test if its possible to import spark
    """
    try:
        import pyspark
        from pyspark import SparkConf, SparkContext
        from pyspark.sql import SparkSession
    except ImportError:
        pytest.fail(
            """Could not import pyspark - is SPARK_HOME and JAVA_HOME set as variables?
                    see https://spark.apache.org/docs/latest/quick-start.html and ensure
                    that your spark instance is configured properly"""
        )


@pytest.mark.spark_test
def test_create_spark_session(spark_session):
    """
    Test if pytest-spark's spark sessions can be properly created
    """
    try:
        from pyspark.sql import SparkSession

        assert isinstance(spark_session, SparkSession)
    except AssertionError:
        pytest.fail(
            """pytest spark_session was not configured properly and could not be created
        is pytest-spark installed and configured properly?"""
        )


@pytest.fixture()
def spark_df(spark_session):
    from datetime import datetime
    from decimal import Decimal

    from pyspark.sql.types import (
        DateType,
        DecimalType,
        IntegerType,
        StringType,
        StructField,
        StructType,
    )

    data2 = [
        ("James", "", "Smith", "36636", "M", 3000, datetime(1980, 1, 2), Decimal(1.5)),
        ("Michael", "Rose", "", "40288", "M", 4000, datetime(1980, 1, 1), Decimal(1.4)),
        (
            "Robert",
            "",
            "Williams",
            "42114",
            "M",
            4000,
            datetime(1980, 1, 3),
            Decimal(1.2),
        ),
        (
            "Maria",
            "Anne",
            "Jones",
            "39192",
            "F",
            4000,
            datetime(1980, 1, 1),
            Decimal(1.0),
        ),
        ("Jen", "Mary", "Brown", "", "F", -1, datetime(1980, 1, 1), Decimal(0.5)),
    ]

    schema = StructType(
        [
            StructField("firstname", StringType(), True),
            StructField("middlename", StringType(), True),
            StructField("lastname", StringType(), True),
            StructField("id", StringType(), True),
            StructField("gender", StringType(), True),
            StructField("salary", IntegerType(), True),
            StructField("da", DateType(), True),
            StructField("nu", DecimalType(), True),
        ]
    )

    return spark_session.createDataFrame(data=data2, schema=schema)


@pytest.mark.spark_test
def test_spark_backend(spark_session, spark_df):
    import visions
    from visions import Date, Float, Integer, Object, StandardSet, String

    tset = StandardSet()
    result = tset.detect_type(spark_df)
    expected = {
        "da": Object,
        "firstname": String,
        "gender": String,
        "id": String,
        "lastname": String,
        "middlename": String,
        "nu": Float,
        "salary": Integer,
    }
    assert result == expected

    tset2 = tset + Date
    result2 = tset2.detect_type(spark_df)
    expected2 = {
        "da": Date,
        "firstname": String,
        "gender": String,
        "id": String,
        "lastname": String,
        "middlename": String,
        "nu": Float,
        "salary": Integer,
    }
    assert result2 == expected2
