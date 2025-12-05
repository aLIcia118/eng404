from copy import deepcopy
from unittest.mock import patch
import pytest

import cities.queries as qry

import os
import pytest

if os.getenv("CI") == "true":
    pytest.skip("Skipping DB tests on CI", allow_module_level=True)


# Helper function to make a new city record for testing.
def _make_city(suffix: str) -> dict:
    c = deepcopy(qry.SAMPLE_CITY)
    c[qry.NAME] = f"{c[qry.NAME]}-{suffix}"
    return c

# This fixture creates a temporary city before each test,
# and deletes it after the test is finished.
@pytest.fixture(scope="function")
def temp_city():
    rec = _make_city("temp")
    new_id = qry.create(rec)
    yield new_id, rec
    try:
        qry.delete(new_id)
    except ValueError:
        pass

# Test that the number of cities increases when we insert a new one.
def test_num_cities():
    old_count = qry.num_cities()
    qry.create(_make_city("count"))
    assert qry.num_cities() == old_count + 1

# Test that create() returns a valid ID and increases count.
def test_good_create():
    old_count = qry.num_cities()
    new_id = qry.create(_make_city("good"))
    assert qry.is_valid_id(new_id)
    assert qry.num_cities() == old_count + 1

# Test that delete() actually removes the city from the DB.
def test_delete(temp_city):
    new_id, _ = temp_city
    qry.delete(new_id)
    cities = qry.read()
    assert new_id not in cities

# Test that deleting a non-existent ID raises an error.
def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete("not-a-real-id")

# Test that read() returns all cities and includes the temp city.
def test_read(temp_city):
    cities = qry.read()
    assert isinstance(cities, dict)
    new_id, rec = temp_city
    assert new_id in cities
    assert cities[new_id][qry.NAME] == rec[qry.NAME]

# If the DB cannot connect, read() should raise ConnectionError.
@patch("cities.queries._can_connect", return_value=False)
def test_read_cant_connect(mock_db):
    with pytest.raises(ConnectionError):
        qry.read()
