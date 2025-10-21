# python
import uuid
import pytest
import cities.queries as qry

@pytest.fixture
def temp_city_record():
    """
    Create a temporary city record with a unique name, yield (id, record),
    then remove it from the in-memory cache in teardown. If it's already
    removed, ignore the KeyError.
    """
    unique_name = f"TempCity-{uuid.uuid4().hex[:8]}"
    record = {qry.NAME: unique_name, qry.STATE_CODE: "ZZ"}
    new_id = qry.create(record)
    yield new_id, record
    try:
        del qry.city_cache[new_id]
    except KeyError:
        pass

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