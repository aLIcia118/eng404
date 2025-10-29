
import pytest
import cities.queries as qry

"""
    Test that raises a ValueError when called
    with an invalid type 
"""

def test_create_with_invalid_type_raises():
    
    with pytest.raises(ValueError):
        qry.create(12345)
"""
    Test that raises a ValueError when the 'name'
    field is missing from the city dictionary.
"""
def test_create_with_missing_name_raises():
    
    with pytest.raises(ValueError):
        qry.create({"state_code": "NY"})

"""
    Test that raises a ValueError when attempting
    to delete a city that does not exist in the database.
"""
def test_delete_nonexistent_city_raises():
    
    with pytest.raises(ValueError):
        qry.delete("not_a_real_id")

"""
    Test that raises a ConnectionError when the database
    connection fails. 
"""
def test_read_connection_error_raises(monkeypatch):
    
    monkeypatch.setattr(qry, "db_connect", lambda _: False)
    with pytest.raises(ConnectionError):
        qry.read()
