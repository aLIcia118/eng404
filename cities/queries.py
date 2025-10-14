#city level data
ID = 'id'
NAME = 'name'
STATE_CODE = 'state_code'

city_cache = {}

SAMPLE_CITY = {
    NAME: 'New York',
    STATE_CODE: 'NY',
}


def num_cities():
    return len(city_cache)


def create(flds: str):
    if not isinstance(flds, dict):
        raise ValueError(f'Bad type for {type(flds)=}')
    if not flds.get(NAME):
        raise ValueError(f'Bad value for {flds.get(NAME)=}')
    new_id = len(city_cache) + 1
    city_cache[new_id] = flds
    return new_id