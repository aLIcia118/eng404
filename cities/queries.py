#This file records city level data

from random import randint

MIN_ID_LEN = 1

ID = 'id'
NAME = 'name'
STATE_CODE = 'state_code'



SAMPLE_CITY = {
    NAME: 'New York',
    STATE_CODE: 'NY',
}

city_cache = {
    1: SAMPLE_CITY,
}

def db_connect(success_ratio: int) -> bool:
    return randint(1, success_ratio) % success_ratio

def is_valid_id(_id: str) -> bool:
    if not isinstance(_id, str):
        return False
    if len(_id) < MIN_ID_LEN:
        return False
    return True


def num_cities() -> int:
    return len(city_cache)


def create(flds: dict) -> str:
    if not isinstance(flds, dict):
        raise ValueError(f'Bad type for {type(flds)=}')
    if not flds.get(NAME):
        raise ValueError(f'Bad value for {flds.get(NAME)=}')
    new_id = str(len(city_cache) + 1)
    city_cache[new_id] = flds
    return new_id

def read() -> dict:
    if not db_connect(3):
        raise ConnectionError('Could not connect to DB.')

    return city_cache

def main():
    print(read())

if __name__ == '__main__':
    main()
