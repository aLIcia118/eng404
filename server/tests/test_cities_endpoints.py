import pytest
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_get_cities_initial():
    """GET /cities should return a list."""
    resp = TEST_CLIENT.get("/cities")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_create_city():
    """POST /cities should create a new city and return its info."""
    payload = {"name": "Testville", "state_code": "TV"}
    resp = TEST_CLIENT.post("/cities", json=payload)

    assert resp.status_code in (200, 201)
    data = resp.get_json()

    assert "id" in data
    assert data["name"] == "Testville"
    assert data["state_code"] == "TV"

    # Save for next tests
    global _CITY_ID
    _CITY_ID = data["id"]


def test_get_city_by_id():
    resp = TEST_CLIENT.get(f"/cities/{_CITY_ID}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == _CITY_ID


def test_update_city():
    """PATCH /cities/<id> should update fields."""
    payload = {"name": "UpdatedCity"}
    resp = TEST_CLIENT.patch(f"/cities/{_CITY_ID}", json=payload)
    assert resp.status_code in (200, 204, 202)

    # Verify update
    resp2 = TEST_CLIENT.get(f"/cities/{_CITY_ID}")
    data = resp2.get_json()
    assert data["name"] == "UpdatedCity"


def test_delete_city():
    """DELETE /cities/<id> should remove the city."""
    resp = TEST_CLIENT.delete(f"/cities/{_CITY_ID}")
    assert resp.status_code in (200, 204)

    # Should now be not found
    resp2 = TEST_CLIENT.get(f"/cities/{_CITY_ID}")
    assert resp2.status_code in (404, 410)
