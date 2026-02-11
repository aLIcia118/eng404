"""
Test suite for load_geo_data.py script

Tests the data loader functionality with mocked database connections.
"""

import pytest
from unittest.mock import patch, MagicMock, call
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from load_geo_data import (
    GeoDataValidator,
    GeoDataLoader,
    SAMPLE_STATES,
    SAMPLE_CITIES,
)


class TestGeoDataValidator:
    """Test the GeoDataValidator class"""

    def test_validate_valid_state(self):
        """Test validation of a valid state"""
        state = {"name": "New York", "code": "NY", "country_code": "USA"}
        is_valid, error = GeoDataValidator.validate_state(state)
        assert is_valid is True
        assert error == ""

    def test_validate_state_missing_name(self):
        """Test validation fails when name is missing"""
        state = {"code": "NY", "country_code": "USA"}
        is_valid, error = GeoDataValidator.validate_state(state)
        assert is_valid is False
        assert "name" in error.lower()

    def test_validate_state_missing_code(self):
        """Test validation fails when code is missing"""
        state = {"name": "New York", "country_code": "USA"}
        is_valid, error = GeoDataValidator.validate_state(state)
        assert is_valid is False
        assert "code" in error.lower()

    def test_validate_state_missing_country_code(self):
        """Test validation fails when country_code is missing"""
        state = {"name": "New York", "code": "NY"}
        is_valid, error = GeoDataValidator.validate_state(state)
        assert is_valid is False
        assert "country_code" in error.lower()

    def test_validate_state_wrong_type(self):
        """Test validation fails when input is not a dict"""
        is_valid, error = GeoDataValidator.validate_state("not a dict")
        assert is_valid is False
        assert "dict" in error.lower()

    def test_validate_state_name_wrong_type(self):
        """Test validation fails when name is not a string"""
        state = {"name": 123, "code": "NY", "country_code": "USA"}
        is_valid, error = GeoDataValidator.validate_state(state)
        assert is_valid is False
        assert "string" in error.lower()

    def test_validate_valid_city(self):
        """Test validation of a valid city"""
        city = {"name": "New York City", "state_code": "NY"}
        is_valid, error = GeoDataValidator.validate_city(city)
        assert is_valid is True
        assert error == ""

    def test_validate_city_missing_name(self):
        """Test validation fails when name is missing"""
        city = {"state_code": "NY"}
        is_valid, error = GeoDataValidator.validate_city(city)
        assert is_valid is False
        assert "name" in error.lower()

    def test_validate_city_missing_state_code(self):
        """Test validation fails when state_code is missing"""
        city = {"name": "New York City"}
        is_valid, error = GeoDataValidator.validate_city(city)
        assert is_valid is False
        assert "state_code" in error.lower()

    def test_validate_city_wrong_type(self):
        """Test validation fails when input is not a dict"""
        is_valid, error = GeoDataValidator.validate_city([])
        assert is_valid is False
        assert "dict" in error.lower()


class TestGeoDataLoader:
    """Test the GeoDataLoader class"""

    def test_loader_initialization(self):
        """Test loader initialization"""
        loader = GeoDataLoader(verbose=False)
        assert loader.verbose is False
        assert loader.loaded_states == 0
        assert loader.loaded_cities == 0
        assert loader.failed_states == 0
        assert loader.failed_cities == 0

    @patch("load_geo_data.state_queries.create")
    def test_load_valid_states(self, mock_create):
        """Test loading valid states"""
        loader = GeoDataLoader(verbose=False)
        states = [
            {"name": "State1", "code": "S1", "country_code": "USA"},
            {"name": "State2", "code": "S2", "country_code": "USA"},
        ]

        loader.load_states(states)

        assert loader.loaded_states == 2
        assert loader.failed_states == 0
        assert mock_create.call_count == 2

    @patch("load_geo_data.state_queries.create")
    def test_load_states_with_invalid_data(self, mock_create):
        """Test loading states with invalid data"""
        loader = GeoDataLoader(verbose=False)
        states = [
            {"name": "Valid State", "code": "VS", "country_code": "USA"},  # Valid
            {"code": "IS"},  # Invalid - missing name and country_code
            {"name": "Another Valid", "code": "AV", "country_code": "USA"},  # Valid
        ]

        loader.load_states(states)

        # Only 2 valid states should be loaded
        assert loader.loaded_states == 2
        assert loader.failed_states == 1
        assert mock_create.call_count == 2

    @patch("load_geo_data.city_queries.create")
    def test_load_valid_cities(self, mock_create):
        """Test loading valid cities"""
        loader = GeoDataLoader(verbose=False)
        cities = [
            {"name": "City1", "state_code": "CA"},
            {"name": "City2", "state_code": "NY"},
        ]

        loader.load_cities(cities)

        assert loader.loaded_cities == 2
        assert loader.failed_cities == 0
        assert mock_create.call_count == 2

    @patch("load_geo_data.city_queries.create")
    def test_load_cities_with_invalid_data(self, mock_create):
        """Test loading cities with invalid data"""
        loader = GeoDataLoader(verbose=False)
        cities = [
            {"name": "Valid City", "state_code": "CA"},  # Valid
            {"name": "Invalid City"},  # Invalid - missing state_code
        ]

        loader.load_cities(cities)

        assert loader.loaded_cities == 1
        assert loader.failed_cities == 1
        assert mock_create.call_count == 1

    @patch("load_geo_data.state_queries.create")
    def test_load_states_handles_exceptions(self, mock_create):
        """Test that loader handles exceptions during state loading"""
        mock_create.side_effect = Exception("Database error")

        loader = GeoDataLoader(verbose=False)
        states = [{"name": "Test", "code": "T", "country_code": "USA"}]

        loader.load_states(states)

        assert loader.loaded_states == 0
        assert loader.failed_states == 1

    @patch("load_geo_data.city_queries.create")
    def test_load_cities_handles_exceptions(self, mock_create):
        """Test that loader handles exceptions during city loading"""
        mock_create.side_effect = Exception("Database error")

        loader = GeoDataLoader(verbose=False)
        cities = [{"name": "Test City", "state_code": "CA"}]

        loader.load_cities(cities)

        assert loader.loaded_cities == 0
        assert loader.failed_cities == 1

    def test_log_respects_verbose_flag(self, capsys):
        """Test that log() respects verbose flag"""
        # With verbose=True
        loader = GeoDataLoader(verbose=True)
        loader.log("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out

        # With verbose=False
        loader = GeoDataLoader(verbose=False)
        loader.log("Test message")
        captured = capsys.readouterr()
        assert "Test message" not in captured.out

    def test_print_summary(self, capsys):
        """Test summary printing"""
        loader = GeoDataLoader(verbose=True)
        loader.loaded_states = 10
        loader.failed_states = 2
        loader.loaded_cities = 25
        loader.failed_cities = 3

        loader.print_summary()

        captured = capsys.readouterr()
        assert "10" in captured.out
        assert "2" in captured.out
        assert "25" in captured.out
        assert "3" in captured.out

    @patch("load_geo_data.state_queries.create")
    @patch("load_geo_data.city_queries.create")
    def test_load_sample_data(self, mock_city_create, mock_state_create):
        """Test loading sample data"""
        loader = GeoDataLoader(verbose=False)
        loader.load_sample_data()

        # Should load 10 sample states and 16 sample cities
        assert loader.loaded_states == 10
        assert loader.loaded_cities == 16
        assert mock_state_create.call_count == 10
        assert mock_city_create.call_count == 16

    @patch("load_geo_data.state_queries.create")
    def test_load_states_skip_duplicate_key_error(self, mock_create):
        """Test that duplicate key errors are handled gracefully"""
        mock_create.side_effect = ValueError("Duplicate key error")

        loader = GeoDataLoader(verbose=False)
        states = [{"name": "Test", "code": "T", "country_code": "USA"}]

        # The error message contains "Duplicate key", so it should be skipped
        loader.load_states(states)

        # With duplicate key error, it should be skipped (not failed)
        assert loader.loaded_states == 0


class TestSampleData:
    """Test sample data consistency"""

    def test_sample_states_have_required_fields(self):
        """Test that all sample states have required fields"""
        for state in SAMPLE_STATES:
            assert "name" in state
            assert "code" in state
            assert "country_code" in state
            assert isinstance(state["name"], str)
            assert isinstance(state["code"], str)
            assert isinstance(state["country_code"], str)

    def test_sample_cities_have_required_fields(self):
        """Test that all sample cities have required fields"""
        for city in SAMPLE_CITIES:
            assert "name" in city
            assert "state_code" in city
            assert isinstance(city["name"], str)
            assert isinstance(city["state_code"], str)

    def test_sample_cities_reference_valid_states(self):
        """Test that all cities reference valid state codes"""
        state_codes = {state["code"] for state in SAMPLE_STATES}
        for city in SAMPLE_CITIES:
            assert city["state_code"] in state_codes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
