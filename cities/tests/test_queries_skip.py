import os
import pytest
import cities.queries as qry

"""
This test verifies that num_cities() can run when DB access is enabled.
We gate it behind an environment flag so CI/devs can turn off DB-dependent
tests easily (e.g., when Mongo isn’t available locally).
"""

@pytest.mark.skipif(os.environ.get("NO_DB") == "1",
                    reason="DB disabled in this environment")
def test_num_cities_runs_when_db_enabled():
    assert isinstance(qry.num_cities(), int)

    