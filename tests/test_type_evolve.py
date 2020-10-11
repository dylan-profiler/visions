from visions.relations.integer_to_datetime import integer_to_datetime_year_month_day
from visions.types.date_time import DateTime


def relations_generator(vtype):
    return [integer_to_datetime_year_month_day(vtype)]


def test_evolve_extend_datetime():
    DateTimeIntYYYYMMDD = DateTime.evolve_type("int_yyyymmdd", relations_generator)
    assert str(DateTimeIntYYYYMMDD) == "DateTime[int_yyyymmdd]"
    assert str(DateTime) == "DateTime"
    assert len(DateTime.get_relations()) == 2
    assert len(DateTimeIntYYYYMMDD.get_relations()) == 3


def test_evolve_replace_datetime():
    DateTimeIntYYYYMMDD = DateTime.evolve_type(
        "int_yyyymmdd_r", relations_generator, replace=True
    )
    assert str(DateTimeIntYYYYMMDD) == "DateTime[int_yyyymmdd_r]"
    assert str(DateTime) == "DateTime"
    assert len(DateTime.get_relations()) == 2
    assert len(DateTimeIntYYYYMMDD.get_relations()) == 1
