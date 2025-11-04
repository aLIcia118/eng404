from unittest.mock import patch
import pytest

import cities.queries as qry

@pytest.fixture(scope='function')
def clean_cache():
    # Start each test with an empty cache
    with patch.dict("cities.queries.city_cache", {}, clear=True):
        yield
    
def temp_city():
    """
    Create a temporary city record for each test and ensure cleanup.
    Returns the new record's id (as a string if create() was updated).
    """
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    yield new_rec_id
    try: 
        qry.delete(new_rec_id)
    except ValueError:
        print("Record Deleted")

def test_num_cities():
    """
    num_cities() should increase by exactly 1 after a successful create().
    We don't assert the exact starting count, only the delta.
    """
    old_count = qry.num_cities()
    qry.create(qry.SAMPLE_CITY)
    assert qry.num_cities() == old_count + 1

def test_good_create():
    """
    create() should return a valid id and increase the count by 1.
    """
    old_count = qry.num_cities()
    new_rec_id = qry.create(qry.SAMPLE_CITY)
    assert qry.is_valid_id(new_rec_id)
    assert qry.num_cities() == old_count + 1

@patch('cities.queries.db_connect', return_value=True, autospec=True)
def test_delete(mock_db_connect, temp_city):
    """
    With db_connect() forced to succeed, delete() should remove the record
    and it should no longer appear in read().
    """
    qry.delete(temp_city)
    assert temp_city not in qry.read()

@patch('cities.queries.db_connect', return_value=True, autospec=True)
def test_delete_not_there(mock_db_connect):
    """
    Deleting a non-existent id should raise ValueError (contract check).
    """
    with pytest.raises(ValueError):
        qry.delete('some value that is not there')

@patch('cities.queries.db_connect', return_value=True, autospec=True)
def test_read(mock_db_connect, temp_city):
    """
    read() should return a mapping/dict of records (per this project's API),
    and the temp record id should be present.
    """
    cities = qry.read()
    assert isinstance(cities, dict)
    assert temp_city in cities

@patch('cities.queries.db_connect', return_value=False, autospec=True)
def test_read_cant_connect(mock_db_connect):
    """
    When db_connect() fails, read() should surface a ConnectionError.
    """
    with pytest.raises(ConnectionError):
        cities = qry.read()
        
