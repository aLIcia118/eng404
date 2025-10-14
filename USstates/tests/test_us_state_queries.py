import pytest
import USstates.queries as qry


def test_create_state():
    count = qry.num_states()
    qry.create(qry.SAMPLE_STATE)
    assert qry.num_states() > count


def test_invalid_state_code():
    with pytest.raises(ValueError):
        qry.create({"name": "InvalidState", "code": "XYZ"})


def test_create_non_dict():
    with pytest.raises(ValueError):
        qry.create("CA")
