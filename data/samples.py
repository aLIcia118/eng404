"""
Centralized sample data for demo purposes when MongoDB is unavailable.
Used across the application to provide consistent fallback data.
"""

# Sample cities data for demo purposes when MongoDB is unavailable
SAMPLE_CITIES_LIST = [
    {"_id": "NYC001", "name": "New York", "state_code": "NY", "population": 8335897},
    {"_id": "NYC002", "name": "Buffalo", "state_code": "NY", "population": 250514},
    {"_id": "NYC003", "name": "Rochester", "state_code": "NY", "population": 211328},
    {"_id": "LAC001", "name": "Los Angeles", "state_code": "CA", "population": 3979576},
    {"_id": "LAC002", "name": "San Francisco", "state_code": "CA", "population": 873965},
    {"_id": "LAC003", "name": "San Diego", "state_code": "CA", "population": 1423851},
    {"_id": "TXC001", "name": "Houston", "state_code": "TX", "population": 2320268},
    {"_id": "TXC002", "name": "Dallas", "state_code": "TX", "population": 1343573},
    {"_id": "TXC003", "name": "Austin", "state_code": "TX", "population": 978908},
]

# Sample cities as dict for faster lookups
SAMPLE_CITIES_DICT = {city["_id"]: city for city in SAMPLE_CITIES_LIST}

# Sample states data for demo purposes when MongoDB is unavailable
SAMPLE_STATES = [
    {"code": "NY", "name": "New York", "country_code": "USA"},
    {"code": "CA", "name": "California", "country_code": "USA"},
    {"code": "TX", "name": "Texas", "country_code": "USA"},
    {"code": "FL", "name": "Florida", "country_code": "USA"},
    {"code": "PA", "name": "Pennsylvania", "country_code": "USA"},
    {"code": "IL", "name": "Illinois", "country_code": "USA"},
    {"code": "OH", "name": "Ohio", "country_code": "USA"},
    {"code": "GA", "name": "Georgia", "country_code": "USA"},
    {"code": "NC", "name": "North Carolina", "country_code": "USA"},
    {"code": "MI", "name": "Michigan", "country_code": "USA"},
]
