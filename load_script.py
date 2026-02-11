from data import db_connect as dbc

CITIES = [
    {"name": "New York", "state_code": "NY", "country": "US"},
    {"name": "Los Angeles", "state_code": "CA", "country": "US"},
    {"name": "Chicago", "state_code": "IL", "country": "US"},
]


def load_cities():
    """
    Insert predefined cities into the database.
    """
    for city in CITIES:
        dbc.create("cities", city)
        print(f"Inserted city: {city['name']}")


def main():
    """
    Entry point for script.
    """
    load_cities()
    print("Finished loading geographic entities.")


if __name__ == "__main__":
    main()
