import pytest
import cities.queries as qry

def test_create_with_invalid_type_raises():
    """Test that qry.create() raises a ValueError when called with an invalid type."""
    with pytest.raises(ValueError):
        qry.create(12345)


def test_create_with_missing_name_raises():
    """Test that qry.create() raises a ValueError when the 'name' field is missing."""
    with pytest.raises(ValueError):
        qry.create({"state_code": "NY"})


def test_delete_nonexistent_city_raises():
    """Test that qry.delete() raises a ValueError when deleting a nonexistent city."""
    with pytest.raises(ValueError):
        qry.delete("not_a_real_id")


def test_read_connection_error_raises(monkeypatch):
    """Test that qry.read() raises a ConnectionError when the database connection fails."""
    # Simulate a failed database connection
    monkeypatch.setattr(qry, "db_connect", lambda _: False)

    with pytest.raises(ConnectionError):
        qry.read()
