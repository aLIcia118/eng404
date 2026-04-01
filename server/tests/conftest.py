import pytest
import server.endpoints as ep


@pytest.fixture
def client():
    """Create a test client for Flask app."""
    return ep.app.test_client()
