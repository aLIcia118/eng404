

import requests

BASE_URL = "http://127.0.0.1:8000"

cities = [
    {"name": "New York", "state_code": "NY"},
    {"name": "Buffalo", "state_code": "NY"},
    {"name": "Los Angeles", "state_code": "CA"},
    {"name": "San Francisco", "state_code": "CA"},
    {"name": "Austin", "state_code": "TX"},
    {"name": "Houston", "state_code": "TX"},
]

def main():
    for city in cities:
        response = requests.post(f"{BASE_URL}/cities", json=city)
        print(f"Loading {city['name']} -> Status: {response.status_code}")

if __name__ == "__main__":
    main()

#test