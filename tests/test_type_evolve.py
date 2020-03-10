from visions.types.date_time import DateTime
from visions.relations.integer_to_datetime import integer_to_datetime_year_month_day


def test_evolve_extend_datetime():
    DateTimeIntYYYYMMDD = DateTime.evolve_extend_relations(
        "int_yyyymmdd", integer_to_datetime_year_month_day
    )
    assert str(DateTimeIntYYYYMMDD) == "DateTime[int_yyyymmdd]"
    assert str(DateTime) == "DateTime"
    assert len(DateTime.get_relations()) == 2
    assert len(DateTimeIntYYYYMMDD.get_relations()) == 3


def test_evolve_replace_datetime():
    DateTimeIntYYYYMMDD = DateTime.evolve_replace_relations(
        "int_yyyymmdd_r", lambda c: [integer_to_datetime_year_month_day(c)]
    )
    assert str(DateTimeIntYYYYMMDD) == "DateTime[int_yyyymmdd_r]"
    assert str(DateTime) == "DateTime"
    assert len(DateTime.get_relations()) == 2
    assert len(DateTimeIntYYYYMMDD.get_relations()) == 1
