# python
import uuid
import pytest
import cities.queries as qry

# avoid same name conflict
_counter = 0
def _next_suffix():
    global _counter
    _counter += 1
    return _counter

@pytest.fixture
def temp_city_record():
    name = f"TempCity-{_next_suffix()}"
    record = {qry.NAME: name, qry.STATE_CODE: "ZZ"}
    new_id = qry.create(record)
    yield new_id, record
    qry.city_cache.pop(new_id, None)

def test_temp_city_fixture_creates_and_cleans(temp_city_record):
    # delete temp instance created before
    new_id, record = temp_city_record
    assert isinstance(new_id, str)
    assert record[qry.NAME].startswith("TempCity-")
    assert new_id in qry.city_cache
    # Delete inside the test to exercise the fixture teardown's ignore-path
    del qry.city_cache[new_id]
    assert new_id not in qry.city_cache

def test_create_raises_on_bad_input():
    # check input validation
    with pytest.raises(ValueError):
        qry.create("not-a-dict")

def test_exist_with_fixture(temp_city_record): # new_id get after creating fixture should be in the cache
    new_id, _ = temp_city_record
    assert new_id in qry.city_cache

def test_read_one_with_fixture(temp_city_record): # test after deleting the record, there should not
    # be any error, nor the record can be gotten again
    new_id, _ = temp_city_record
    stored = qry.city_cache.get(new_id)
    assert stored is not None
    assert qry.NAME in stored and qry.STATE_CODE in stored

def test_delete_with_fixture(temp_city_record): # test getting a key that doesn't exist
    new_id, _ = temp_city_record
    qry.city_cache.pop(new_id, None)
    assert qry.city_cache.get(new_id) is None

def test_not_exist_without_fixture():
    assert qry.city_cache.get("non-existent-id") is None