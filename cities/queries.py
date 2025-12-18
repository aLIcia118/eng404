from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict
from uuid import uuid4

from data import db_connect as dbc

MIN_ID_LEN = 1
CITY_COLLECTION = "cities"
ID = "id"
NAME = "name"
STATE_CODE = "state_code"

SAMPLE_CITY = {
    NAME: "TempCity",
    STATE_CODE: "ZZ",
}

# in-memory cache: key = internal city id, value = city record
city_cache: dict[str, dict[str, Any]] = {}


def _can_connect() -> bool:
    """
    Small helper so tests can monkeypatch connectivity.
    Prefer dbc.ping() if present; otherwise fall back to a simple read.
    """
    try:
        if hasattr(dbc, "ping"):
            return bool(dbc.ping())
        _ = dbc.read(CITY_COLLECTION)
        return True
    except Exception:
        return False


def is_valid_id(_id: str) -> bool:
    """Return True if `_id` looks like a valid city id."""
    return isinstance(_id, str) and len(_id) >= MIN_ID_LEN


def _next_id() -> str:
    """Generate a new internal city id."""
    return str(uuid4())


def num_cities() -> int:
    """Return the number of cities currently known (via read())."""
    return len(read())


def create(flds: dict[str, Any]) -> str:
    """
    Create a new city both in the in-memory cache and best-effort in the DB.

    Args:
        flds: a mapping with at least NAME and STATE_CODE.

    Returns:
        The newly generated internal city id.

    Raises:
        ValueError: if required fields are missing or flds is not a dict.
    """
    if not isinstance(flds, dict):
        raise ValueError(f"Bad type for {type(flds)=}")
    if not flds.get(NAME):
        raise ValueError("Missing city name")
    if not flds.get(STATE_CODE):
        raise ValueError("Missing state code")

    new_id = _next_id()
    rec = deepcopy(flds)
    rec[ID] = new_id
    city_cache[new_id] = rec

    # Best-effort write to DB; failures are swallowed so cache still works.
    try:
        dbc.create(CITY_COLLECTION, flds)
    except Exception:
        pass

    return new_id


def delete(*args: str) -> bool:
    """
    Delete a city.

    Usage:
        delete(city_id)                 -> delete from cache (and try DB)
        delete(name, state_code)       -> delete from DB and cache

    Raises:
        ValueError: if the city does not exist for the given key(s).
        TypeError: if called with the wrong number of arguments.
    """
    # Case 1: Delete by internal city ID from the in-memory cache (used by older tests)
    if len(args) == 1:
        city_id = args[0]
        if city_id not in city_cache:
            raise ValueError(f"No such city: {city_id}")
        rec = city_cache.pop(city_id)
        try:
            if rec and NAME in rec and STATE_CODE in rec:
                dbc.delete(
                    CITY_COLLECTION,
                    {NAME: rec[NAME], STATE_CODE: rec[STATE_CODE]},
                )
        except Exception:
            pass
        return True

    # Case 2: Delete by city name and state code, removing from both MongoDB and the local cache
    if len(args) == 2:
        name, state_code = args
        deleted = dbc.delete(
            CITY_COLLECTION,
            {NAME: name, STATE_CODE: state_code},
        )
        if deleted < 1:
            raise ValueError(f"City not found: {name}, {state_code}")

        ids_to_del: list[str] = []
        for cid, rec in city_cache.items():
            if rec.get(NAME) == name and rec.get(STATE_CODE) == state_code:
                ids_to_del.append(cid)
        for cid in ids_to_del:
            del city_cache[cid]
        return True

    # Case 3: Invalid argument count — enforce correct usage
    raise TypeError("delete() takes 1 or 2 positional arguments")

def update(city_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    """
    Update fields for a city identified by its internal ID.

    Returns:
        The updated city record.

    Raises:
        ValueError: if the city_id is invalid or not found,
                    or updates is not a dict.
    """
    if not is_valid_id(city_id):
        raise ValueError(f"Invalid city id: {city_id!r}")
    if not isinstance(updates, dict):
        raise ValueError(f"Bad type for updates: {type(updates)!r}")

    cities = read()  # ensure cache is loaded and DB reachable
    rec = cities.get(city_id)
    if rec is None:
        raise ValueError(f"No such city: {city_id}")

    # compute new record
    new_rec = deepcopy(rec)
    new_rec.update(updates)
    city_cache[city_id] = new_rec

    # best-effort update in DB
    try:
        dbc.update(
            CITY_COLLECTION,
            {NAME: rec.get(NAME), STATE_CODE: rec.get(STATE_CODE)},
            updates,
        )
    except Exception:
        pass

    return new_rec

def read() -> dict[str, dict[str, Any]]:
    """
    Load cities from DB into the cache (if needed) and return the cache.

    Raises:
        ConnectionError: if the DB is not reachable.
    """
    if not _can_connect():
        raise ConnectionError("cannot connect")

    if city_cache:
        return city_cache

    recs = dbc.read(CITY_COLLECTION)
    for rec in recs:
        rec = dict(rec)
        cid = rec.get(ID) or _next_id()
        rec[ID] = cid
        city_cache[cid] = rec
    return city_cache

def read_one(city_id: str) -> dict[str, Any] | None:
    """
    Return a single city record by its internal ID, or None if not found.

    Raises:
        ValueError: if the id is clearly invalid.
    """
    if not is_valid_id(city_id):
        raise ValueError(f"Invalid city id: {city_id!r}")

    cities = read()  # ensures cache is populated (and DB reachable)
    return cities.get(city_id)


def main() -> None:
    cities = read()
    print(cities)


if __name__ == "__main__":
    main()