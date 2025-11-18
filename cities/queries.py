from __future__ import annotations
from copy import deepcopy
from random import randint
from data import db_connect as dbc
from uuid import uuid4

MIN_ID_LEN = 1
CITY_COLLECTION = "cities"
ID = "id"
NAME = "name"
STATE_CODE = "state_code"

SAMPLE_CITY = {
    NAME: "TempCity",
    STATE_CODE: "ZZ",
}

city_cache: dict[str, dict] = {}

# def db_connect(success_ratio: int) -> bool:
#     """Legacy / test hook: simulate whether DB is reachable."""
#     val = randint(1, success_ratio)
#     if val == 3:
#         return False
#     return True

def _can_connect() -> bool:
    try:
        if hasattr(dbc, "ping"):
            return bool(dbc.ping())
        _ = dbc.read(CITY_COLLECTION)  
        return True
    except Exception:
        return False

def is_valid_id(_id: str) -> bool:
    return isinstance(_id, str) and len(_id) >= MIN_ID_LEN


def _next_id() -> str:
    return str(uuid4())


def num_cities() -> int:
    # return len(city_cache)
    return len(read())


def create(flds: dict) -> str:
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
    try:
        dbc.create(CITY_COLLECTION, flds)
    except Exception:
        pass
    return new_id


def delete(*args):
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


def read() -> dict[str, dict]:
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


def read_one(city_id: str) -> dict | None:
    # return city_cache.get(city_id)
    #return dbc.read(CITY_COLLECTION)
    """
    Return a single city record by its internal ID, or None if not found.
    """
    if not is_valid_id(city_id):
        raise ValueError(f"Invalid city id: {city_id!r}")

    cities = read()  # ensures cache is populated (and DB reachable)
    return cities.get(city_id)


def main():
    cities = read()
    print(cities)

if __name__ == "__main__":
    main()
