from unittest.mock import patch
import pytest
import cities.queries as qry


def test_read_raises_when_db_connect_fails():
    # db_connect fail
    with patch("cities.queries.randint", return_value=3):
        with pytest.raises(ConnectionError):
            qry.read()


def test_read_succeeds_when_db_connect_succeeds():
    #db_connect work
    with patch("cities.queries.randint", return_value=2):
        result = qry.read()
        assert isinstance(result, dict)


def test_create_with_isolated_cache_via_patch_dict():
    # use a clean cache
    with patch.dict("cities.queries.city_cache", {}, clear=True):
        new_id = qry.create({qry.NAME: "TempCity", qry.STATE_CODE: "ZZ"})
        assert new_id == "1"
        assert qry.city_cache[new_id][qry.NAME] == "TempCity"


def test_main_prints_result(monkeypatch):
    # fake print and make db_connect work
    with patch("cities.queries.randint", return_value=2):
        printed = []
        #help to verify print output
        def fake_print(x):
            printed.append(x)

        monkeypatch.setattr("builtins.print", fake_print)
        qry.main()
        assert printed and isinstance(printed[0], dict)
