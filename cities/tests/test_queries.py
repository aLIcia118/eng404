import pytest

import cities.queries as qry


@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_for_num_cities():
    assert qry.num_cities() == len(qry.cities)


def test_num_cities():
    old_count = qry.num_cities()
    qry.create(qry.SAMPLE_CITY)
    assert qry.num_cities() == old_count + 1


def test_good_create():
    old_count = qry.num_cities()
    assert qry.create(qry.SAMPLE_CITY) >= 1
    assert qry.num_cities() > old_count


def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})


def test_create_bad_param_type():
    with pytest.raises(ValueError):
        qry.create(17)