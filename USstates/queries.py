from functools import wraps
from time import time
from typing import Any

import data.db_connect as dbc

STATE_COLLECTION = 'states'
MIN_ID_LEN = 1

ID = 'id'
NAME = 'name'
CODE = 'code'
COUNTRY_CODE = 'country_code'

SAMPLE_CODE = 'NY'
SAMPLE_COUNTRY = 'USA'
SAMPLE_KEY = (SAMPLE_CODE, SAMPLE_COUNTRY)
SAMPLE_STATE = {
    NAME: 'New York',
    CODE: SAMPLE_CODE,
    COUNTRY_CODE: SAMPLE_COUNTRY,
}

cache = None
# Cache timestamp for tracking freshness
cache_timestamp: float = 0.0


def clear_cache() -> None:
    """Clear the in-memory state cache and timestamp."""
    global cache, cache_timestamp
    cache = None
    cache_timestamp = 0.0


def is_cache_fresh(max_age_seconds: float = 3600.0) -> bool:
    """Check if cache is fresh (within max_age_seconds old)."""
    return cache is not None and (time() - cache_timestamp) < max_age_seconds


def _refresh_cache_timestamp() -> None:
    """Update cache timestamp to current time."""
    global cache_timestamp
    cache_timestamp = time()


def needs_cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global cache
        if not cache:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


def is_valid_id(_id: str) -> bool:
    """Return True if `_id` looks like a valid state id."""
    return isinstance(_id, str) and len(_id) >= MIN_ID_LEN


@needs_cache
def count() -> int:
    return len(cache)


@needs_cache
def create(flds: dict[str, Any]) -> str:
    if not isinstance(flds, dict):
        raise ValueError(f'Bad type for {type(flds)=}')
    code = flds.get(CODE)
    country_code = flds.get(COUNTRY_CODE)
    if not flds.get(NAME):
        raise ValueError(f'Bad value for {flds.get(NAME)=}')
    if not code:
        raise ValueError(f'Bad value for {code=}')
    if not country_code:
        raise ValueError(f'Bad value for {country_code=}')

    if (code, country_code) in cache:
        raise ValueError(f'Duplicate key: {code=}; {country_code=}')

    res = dbc.create(STATE_COLLECTION, flds)

    # dbc.create may return InsertOneResult, ObjectId, or a string id.
    if hasattr(res, "inserted_id"):
        new_id = res.inserted_id
    else:
        new_id = res

    new_id = str(new_id)
    load_cache()
    return new_id


def delete(code: str, cntry_code: str) -> bool:
    ret = dbc.delete(STATE_COLLECTION, {CODE: code, COUNTRY_CODE: cntry_code})
    if ret < 1:
        raise ValueError(f'State not found: {code}, {cntry_code}')
    load_cache()
    return ret


@needs_cache
def read() -> list[dict[str, Any]]:
    out = []
    for state in cache.values():
        s = dict(state)
        if dbc.MONGO_ID in s:
            s[dbc.MONGO_ID] = str(s[dbc.MONGO_ID])
        out.append(s)
    return out



def load_cache():
    global cache
    cache = {}
    states = dbc.read(STATE_COLLECTION)
    for state in states:
        cache[(state[CODE], state[COUNTRY_CODE])] = state
    _refresh_cache_timestamp()


def main():
    create(SAMPLE_STATE)
    print(read())


if __name__ == '__main__':
    main()