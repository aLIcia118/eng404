from unittest.mock import patch
import pytest

import cities.queries as qry


@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_for_num_cities():
    assert qry.num_cities() == len(qry.city_cache)


def test_num_cities():
    old_count = qry.num_cities()
    qry.create(qry.SAMPLE_CITY)
    assert qry.num_cities() == old_count + 1


def test_good_create():
    old_count = qry.num_cities()
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1


def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})


def test_create_bad_param_type():
    with pytest.raises(ValueError):
        qry.create(17)

@patch('cities.queries.db_connect', return_value=True)
def test_read(mocj_db_connect):
    cities = qry.read()
    assert isinstance(cities, dict)
    assert len(cities) > 1

