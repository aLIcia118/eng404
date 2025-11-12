from copy import deepcopy
from unittest.mock import patch
import pytest

import cities.queries as qry


def _make_city(suffix: str) -> dict:
    c = deepcopy(qry.SAMPLE_CITY)
    c[qry.NAME] = f"{c[qry.NAME]}-{suffix}"
    return c


@pytest.fixture(scope="function")
def temp_city():
    rec = _make_city("temp")
    new_id = qry.create(rec)
    yield new_id, rec
    try:
        qry.delete(new_id)
    except ValueError:
        pass


def test_num_cities():
    old_count = qry.num_cities()
    qry.create(_make_city("count"))
    assert qry.num_cities() == old_count + 1


def test_good_create():
    old_count = qry.num_cities()
    new_id = qry.create(_make_city("good"))
    assert qry.is_valid_id(new_id)
    assert qry.num_cities() == old_count + 1


def test_delete(temp_city):
    new_id, _ = temp_city
    qry.delete(new_id)
    cities = qry.read()
    assert new_id not in cities


def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete("not-a-real-id")


def test_read(temp_city):
    cities = qry.read()
    assert isinstance(cities, dict)
    new_id, rec = temp_city
    assert new_id in cities
    assert cities[new_id][qry.NAME] == rec[qry.NAME]


@patch("cities.queries._can_connect", return_value=False)
def test_read_cant_connect(mock_db):
    with pytest.raises(ConnectionError):
        qry.read()
