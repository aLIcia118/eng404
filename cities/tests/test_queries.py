import pytest

import cities.queries as qry

def test_create():
    with pytest.raises(ValueError):
        qry.create(17)