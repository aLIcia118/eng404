from functools import wraps

import data.db_connect as dbc
from data.db_connect import is_valid_id  # noqa F401

STATE_COLLECTION = 'states'

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


def needs_cache(fn, *args, **kwargs):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not cache:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


@needs_cache
def count() -> int:
    return len(cache)


@needs_cache
def create(flds: dict) -> str:
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
    print(f'{new_id=}')
    load_cache()
    return new_id


def delete(code: str, cntry_code: str) -> bool:
    ret = dbc.delete(STATE_COLLECTION, {CODE: code, COUNTRY_CODE: cntry_code})
    if ret < 1:
        raise ValueError(f'State not found: {code}, {cntry_code}')
    load_cache()
    return ret


@needs_cache
def read() -> list[dict]:
    out = []
    for state in cache.values():
        s = dict(state)
        if "_id" in s:
            s["_id"] = str(s["_id"])
        out.append(s)
    return out



def load_cache():
    global cache
    cache = {}
    states = dbc.read(STATE_COLLECTION)
    for state in states:
        cache[(state[CODE], state[COUNTRY_CODE])] = state


def main():
    create(SAMPLE_STATE)
    print(read())


if __name__ == '__main__':
    main()