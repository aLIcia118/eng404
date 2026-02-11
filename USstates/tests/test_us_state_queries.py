from copy import deepcopy

from unittest.mock import patch
import pytest

import USstates.queries as qry


# Use a temp code that should never exist in the real dataset.
# Keep format consistent with state codes (2 letters).
TEMP_CODE = "ZZ"


def get_temp_rec():
    rec = deepcopy(qry.SAMPLE_STATE)
    rec[qry.CODE] = TEMP_CODE
    # country_code stays the same as SAMPLE_STATE (likely "USA")
    return rec


@pytest.fixture(scope='function')
def temp_state_no_del():
    temp_rec = get_temp_rec()
    qry.create(temp_rec)
    return temp_rec


@pytest.fixture(scope='function')
def temp_state():
    temp_rec = get_temp_rec()
    new_rec_id = qry.create(temp_rec)
    yield new_rec_id
    try:
        qry.delete(temp_rec[qry.CODE], temp_rec[qry.COUNTRY_CODE])
    except ValueError:
        print('The record was already deleted.')


@pytest.mark.skip('This is an example of a bad test!')
def test_bad_test_for_count():
    assert qry.count() == len(qry.cache)


def test_count():
    old_count = qry.count()
    temp_rec = get_temp_rec()
    qry.create(temp_rec)
    assert qry.count() == old_count + 1
    qry.delete(temp_rec[qry.CODE], temp_rec[qry.COUNTRY_CODE])


def test_good_create():
    old_count = qry.count()
    temp_rec = get_temp_rec()
    new_rec_id = qry.create(temp_rec)
    assert qry.is_valid_id(new_rec_id)
    assert qry.count() == old_count + 1
    qry.delete(temp_rec[qry.CODE], temp_rec[qry.COUNTRY_CODE])


def test_create_dup_key():
    temp_rec = get_temp_rec()
    qry.create(temp_rec)
    with pytest.raises(ValueError):
        qry.create(get_temp_rec())
    qry.delete(temp_rec[qry.CODE], temp_rec[qry.COUNTRY_CODE])


def test_create_bad_name():
    with pytest.raises(ValueError):
        qry.create({})


def test_create_bad_param_type():
    with pytest.raises(ValueError):
        qry.create(17)


def test_delete(temp_state_no_del):
    ret = qry.delete(temp_state_no_del[qry.CODE],
                     temp_state_no_del[qry.COUNTRY_CODE])
    assert ret == 1


def test_delete_not_there():
    with pytest.raises(ValueError):
        qry.delete('some state code that is not there', 'not a country code')


def test_read(temp_state):
    states = qry.read()
    assert isinstance(states, list)
    assert all(isinstance(s, dict) for s in states)

    temp_rec = get_temp_rec()
    assert any(
        s.get(qry.CODE) == temp_rec[qry.CODE] and s.get(qry.COUNTRY_CODE) == temp_rec[qry.COUNTRY_CODE]
        for s in states
    )