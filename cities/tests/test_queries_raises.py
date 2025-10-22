
import pytest
import cities.queries as qry

def test_create_with_invalid_type_raises():
    
    with pytest.raises(ValueError):
        qry.create(12345)

def test_create_with_missing_name_raises():
    
    with pytest.raises(ValueError):
        qry.create({"state_code": "NY"})

def test_delete_nonexistent_city_raises():
    
    with pytest.raises(ValueError):
        qry.delete("not_a_real_id")

def test_read_connection_error_raises(monkeypatch):
    
    monkeypatch.setattr(qry, "db_connect", lambda _: False)
    with pytest.raises(ConnectionError):
        qry.read()
