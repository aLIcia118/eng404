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
    new_id = dbc.create(STATE_COLLECTION, flds)
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
def read() -> dict:
    return cache


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