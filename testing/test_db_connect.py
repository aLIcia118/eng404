from unittest.mock import patch
from data.db_connect import needs_db


def test_needs_db_calls_connect_db_once():
    # Patch connect_db so we don't actually hit MongoDB
    with patch("data.db_connect.connect_db") as mock_connect:
        @needs_db
        def add(a, b):
            return a + b

        result = add(2, 3)

        # Decorator should call connect_db before running the function
        mock_connect.assert_called_once()
        # And the wrapped function still returns the correct value
        assert result == 5
