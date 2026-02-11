"""
Script to load geographical entities (states and cities) into MongoDB.

This script:
- Reads geographical data (states and cities)
- Validates data according to database schema
- Inserts data into MongoDB collections
- Provides detailed error reporting and validation
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

# Import database functions
from data import db_connect as dbc
from USstates import queries as state_queries
from cities import queries as city_queries


# Sample geographical data
SAMPLE_STATES = [
    {"name": "New York", "code": "NY", "country_code": "USA"},
    {"name": "California", "code": "CA", "country_code": "USA"},
    {"name": "Texas", "code": "TX", "country_code": "USA"},
    {"name": "Florida", "code": "FL", "country_code": "USA"},
    {"name": "Pennsylvania", "code": "PA", "country_code": "USA"},
    {"name": "Illinois", "code": "IL", "country_code": "USA"},
    {"name": "Ohio", "code": "OH", "country_code": "USA"},
    {"name": "Georgia", "code": "GA", "country_code": "USA"},
    {"name": "North Carolina", "code": "NC", "country_code": "USA"},
    {"name": "Michigan", "code": "MI", "country_code": "USA"},
]

SAMPLE_CITIES = [
    # New York
    {"name": "New York City", "state_code": "NY"},
    {"name": "Buffalo", "state_code": "NY"},
    {"name": "Rochester", "state_code": "NY"},
    {"name": "Yonkers", "state_code": "NY"},
    # California
    {"name": "Los Angeles", "state_code": "CA"},
    {"name": "San Francisco", "state_code": "CA"},
    {"name": "San Diego", "state_code": "CA"},
    {"name": "San Jose", "state_code": "CA"},
    # Texas
    {"name": "Houston", "state_code": "TX"},
    {"name": "Dallas", "state_code": "TX"},
    {"name": "Austin", "state_code": "TX"},
    {"name": "San Antonio", "state_code": "TX"},
    # Florida
    {"name": "Miami", "state_code": "FL"},
    {"name": "Tampa", "state_code": "FL"},
    {"name": "Orlando", "state_code": "FL"},
    {"name": "Jacksonville", "state_code": "FL"},
]


class GeoDataValidator:
    """Validates geographical data against schema requirements."""

    @staticmethod
    def validate_state(state: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate a state record.

        Args:
            state: State dictionary to validate

        Returns:
            tuple of (is_valid, error_message)
        """
        if not isinstance(state, dict):
            return False, f"State must be a dict, got {type(state)}"

        if not state.get("name"):
            return False, "State must have a 'name' field"

        if not isinstance(state.get("name"), str):
            return False, f"State name must be a string, got {type(state.get('name'))}"

        if not state.get("code"):
            return False, "State must have a 'code' field"

        if not isinstance(state.get("code"), str):
            return False, f"State code must be a string, got {type(state.get('code'))}"

        if not state.get("country_code"):
            return False, "State must have a 'country_code' field"

        if not isinstance(state.get("country_code"), str):
            return False, f"Country code must be a string, got {type(state.get('country_code'))}"

        # Validate state code format (should be 2 chars typically)
        if len(state.get("code", "")) < 1:
            return False, "State code cannot be empty"

        return True, ""

    @staticmethod
    def validate_city(city: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate a city record.

        Args:
            city: City dictionary to validate

        Returns:
            tuple of (is_valid, error_message)
        """
        if not isinstance(city, dict):
            return False, f"City must be a dict, got {type(city)}"

        if not city.get("name"):
            return False, "City must have a 'name' field"

        if not isinstance(city.get("name"), str):
            return False, f"City name must be a string, got {type(city.get('name'))}"

        if not city.get("state_code"):
            return False, "City must have a 'state_code' field"

        if not isinstance(city.get("state_code"), str):
            return False, f"State code must be a string, got {type(city.get('state_code'))}"

        return True, ""


class GeoDataLoader:
    """Loads geographical data into MongoDB."""

    def __init__(self, verbose: bool = True):
        """
        Initialize the loader.

        Args:
            verbose: If True, print detailed progress and error messages
        """
        self.verbose = verbose
        self.loaded_states: int = 0
        self.loaded_cities: int = 0
        self.failed_states: int = 0
        self.failed_cities: int = 0
        self.validator = GeoDataValidator()

    def state_exists(self, state: Dict[str, Any]) -> bool:
        return dbc.read_one("USstates", {"code": state["code"]}) is not None

    def city_exists(self, city: Dict[str, Any]) -> bool:
        return dbc.read_one(
            "cities",
            {"name": city["name"], "state_code": city["state_code"]}
        ) is not None

    def log(self, message: str) -> None:
        """Print a message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def load_states(self, states: List[Dict[str, Any]]) -> None:
        """
        Load states into the database.

        Args:
            states: List of state dictionaries
        """
        self.log(f"\n{'='*60}")
        self.log(f"Loading {len(states)} states...")
        self.log('='*60)

        for idx, state in enumerate(states, 1):
            # Validate state
            is_valid, error_msg = self.validator.validate_state(state)

            if not is_valid:
                self.log(f"[FAILED] State #{idx}: {error_msg}")
                self.log(f"  Data: {state}")
                self.failed_states += 1
                continue

            # Check if already exists
            if self.state_exists(state):
                self.log(f"[SKIPPED] State #{idx} already exists: {state['code']}")
                continue
            
            try:
                state_queries.create(state)
                self.log(f"[✓] State #{idx}: {state['name']} ({state['code']})")
                self.loaded_states += 1
            except ValueError as e:
                # Handle duplicate key errors and other validation errors
                if "Duplicate key" in str(e):
                    self.log(f"[SKIPPED] State #{idx} (already exists): {state['code']}")
                else:
                    self.log(f"[FAILED] State #{idx}: {e}")
                    self.failed_states += 1
            except Exception as e:
                self.log(f"[ERROR] State #{idx} ({state.get('name')}): {e}")
                self.failed_states += 1

    def load_cities(self, cities: List[Dict[str, Any]]) -> None:
        """
        Load cities into the database.

        Args:
            cities: List of city dictionaries
        """
        self.log(f"\n{'='*60}")
        self.log(f"Loading {len(cities)} cities...")
        self.log('='*60)

        for idx, city in enumerate(cities, 1):
            # Validate city
            is_valid, error_msg = self.validator.validate_city(city)

            if not is_valid:
                self.log(f"[FAILED] City #{idx}: {error_msg}")
                self.log(f"  Data: {city}")
                self.failed_cities += 1
                continue

            # Check if already exists
            if self.city_exists(city):
                self.log(f"[SKIPPED] City #{idx} already exists: {city['name']}")
                continue
            
            try:
                city_queries.create(city)
                self.log(f"[✓] City #{idx}: {city['name']} ({city['state_code']})")
                self.loaded_cities += 1
            except Exception as e:
                self.log(f"[ERROR] City #{idx} ({city.get('name')}): {e}")
                self.failed_cities += 1

    def print_summary(self) -> None:
        """Print a summary of the loading operation."""
        self.log(f"\n{'='*60}")
        self.log("LOADING SUMMARY")
        self.log('='*60)
        self.log(f"States loaded:   {self.loaded_states}")
        self.log(f"States failed:   {self.failed_states}")
        self.log(f"Cities loaded:   {self.loaded_cities}")
        self.log(f"Cities failed:   {self.failed_cities}")
        self.log('='*60)

    def load_from_json_file(self, filepath: str) -> None:
        """
        Load states and cities from a JSON file.

        Expected JSON format:
        {
            "states": [...],
            "cities": [...]
        }

        Args:
            filepath: Path to JSON file
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            states = data.get("states", [])
            cities = data.get("cities", [])

            if states:
                self.load_states(states)

            if cities:
                self.load_cities(cities)

        except FileNotFoundError:
            self.log(f"Error: File not found: {filepath}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.log(f"Error: Invalid JSON in {filepath}: {e}")
            sys.exit(1)

    def load_sample_data(self) -> None:
        """Load the sample states and cities."""
        self.load_states(SAMPLE_STATES)
        self.load_cities(SAMPLE_CITIES)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Load geographical data (states and cities) into MongoDB"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="Load data from a JSON file (format: {\"states\": [...], \"cities\": [...]})"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Load sample US states and cities data"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output (quiet mode)"
    )

    args = parser.parse_args()

    # Default to sample data if no option specified
    if not args.json and not args.sample:
        args.sample = True

    # Check database connection
    try:
        if not dbc.ping():
            print("Error: Cannot connect to MongoDB. Please ensure MongoDB is running.")
            sys.exit(1)
        print("✓ Connected to MongoDB")
    except Exception as e:
        print(f"Error: Failed to connect to MongoDB: {e}")
        sys.exit(1)

    # Create loader
    loader = GeoDataLoader(verbose=not args.quiet)

    try:
        # Load data based on arguments
        if args.json:
            loader.log(f"Loading from JSON file: {args.json}")
            loader.load_from_json_file(args.json)
        elif args.sample:
            loader.log("Loading sample data...")
            loader.load_sample_data()

        # Print summary
        loader.print_summary()

        # Exit with appropriate code
        if loader.failed_states > 0 or loader.failed_cities > 0:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\nLoading interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during loading: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
