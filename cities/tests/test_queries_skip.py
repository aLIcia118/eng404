import os
import pytest
import cities.queries as qry

@pytest.mark.skipif(os.environ.get("NO_DB") == "1",
                    reason="DB disabled in this environment")
def test_num_cities_runs_when_db_enabled():
    assert isinstance(qry.num_cities(), int)

    