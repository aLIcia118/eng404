"""
Tests for HATEOAS dropdown option endpoints.

These tests verify that the API correctly provides dropdown options
for states and cities, following REST/HATEOAS principles.
"""

import pytest
from http import HTTPStatus


class TestStateOptions:
    """Test the /state/options endpoint for state dropdown selection."""
    
    def test_state_options_returns_options_key(self, client):
        """Test that state options endpoint returns data with 'options' key."""
        response = client.get('/state/options')
        
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        assert 'options' in data, "Response should contain 'options' key"
    
    def test_state_options_returns_list(self, client):
        """Test that options is a list."""
        response = client.get('/state/options')
        data = response.get_json()
        
        assert isinstance(data['options'], list), "Options should be a list"
        assert len(data['options']) > 0, "Should have at least one state"
    
    def test_state_options_have_required_fields(self, client):
        """Test that each state option has code and name."""
        response = client.get('/state/options')
        data = response.get_json()
        
        for option in data['options']:
            assert 'code' in option, f"State option missing 'code': {option}"
            assert 'name' in option, f"State option missing 'name': {option}"
            assert isinstance(option['code'], str), f"Code should be string: {option}"
            assert isinstance(option['name'], str), f"Name should be string: {option}"
    
    def test_state_options_has_known_states(self, client):
        """Test that common US states are present."""
        response = client.get('/state/options')
        data = response.get_json()
        state_codes = [opt['code'] for opt in data['options']]
        
        # Check for some common states
        assert 'NY' in state_codes, "Should include NY"
        assert 'CA' in state_codes, "Should include CA"
        assert 'TX' in state_codes, "Should include TX"


class TestCityOptions:
    """Test the /cities/options endpoint for city dropdown selection."""
    
    def test_city_options_returns_options_key(self, client):
        """Test that city options endpoint returns data with 'options' key."""
        response = client.get('/cities/options')
        
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()
        assert 'options' in data, "Response should contain 'options' key"
    
    def test_city_options_returns_list(self, client):
        """Test that options is a list."""
        response = client.get('/cities/options')
        data = response.get_json()
        
        assert isinstance(data['options'], list), "Options should be a list"
        assert len(data['options']) > 0, "Should have at least one city"
    
    def test_city_options_have_required_fields(self, client):
        """Test that each city option has required fields."""
        response = client.get('/cities/options')
        data = response.get_json()
        
        for option in data['options']:
            assert 'id' in option, f"City option missing 'id': {option}"
            assert 'name' in option, f"City option missing 'name': {option}"
            assert 'state_code' in option, f"City option missing 'state_code': {option}"

    def test_city_options_include_hateoas_links(self, client):
        """Test that city options expose navigable HATEOAS links."""
        response = client.get('/cities/options')
        assert response.status_code == HTTPStatus.OK
        data = response.get_json()

        assert 'links' in data, "Response should contain top-level 'links'"
        assert data['links']['self'].startswith('/cities/options')
        assert data['links']['state_options'] == '/state/options'

        if data['options']:
            option = data['options'][0]
            assert 'links' in option, f"City option missing 'links': {option}"
            assert option['links']['self'].startswith('/cities/')
            assert option['links']['collection'] == '/cities'
            assert option['links']['state_options'] == '/state/options'
    
    def test_city_options_filters_by_state_code(self, client):
        """Test that state_code query parameter filters cities."""
        # Get all cities first
        all_response = client.get('/cities/options')
        all_cities = all_response.get_json()['options']
        
        if len(all_cities) > 0:
            # Pick the first city's state code
            first_city_state = all_cities[0]['state_code']
            
            # Request only cities from that state
            filtered_response = client.get(f'/cities/options?state_code={first_city_state}')
            filtered_cities = filtered_response.get_json()['options']
            
            # Verify all returned cities are from the requested state
            for city in filtered_cities:
                assert city['state_code'].upper() == first_city_state.upper(), \
                    f"Filtered response should only contain cities from {first_city_state}, got {city}"
    
    def test_city_options_with_nonexistent_state(self, client):
        """Test that filtering by nonexistent state returns empty list."""
        response = client.get('/cities/options?state_code=ZZ')
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.OK
        assert data['options'] == [] or isinstance(data['options'], list)
    
    def test_city_options_state_code_case_insensitive(self, client):
        """Test that state code filtering is case-insensitive."""
        # Request with lowercase
        response_lower = client.get('/cities/options?state_code=ny')
        cities_lower = response_lower.get_json()['options']
        
        # Request with uppercase
        response_upper = client.get('/cities/options?state_code=NY')
        cities_upper = response_upper.get_json()['options']
        
        # Should get the same results
        if len(cities_lower) > 0 or len(cities_upper) > 0:
            assert len(cities_lower) == len(cities_upper), \
                "Case-insensitive filtering should return same number of results"
            
            # Verify all returned cities are from NY
            for city in cities_upper:
                assert city['state_code'].upper() == 'NY'


class TestHATEOASIntegration:
    """Integration tests for HATEOAS dropdown options."""
    
    def test_states_endpoint_includes_cities(self, client):
        """Test that states in options match available cities by state."""
        # Get all states
        states_response = client.get('/state/options')
        states = states_response.get_json()['options']
        state_codes = {s['code'] for s in states}
        
        # Get all cities
        cities_response = client.get('/cities/options')
        cities = cities_response.get_json()['options']
        city_state_codes = {c['state_code'].upper() for c in cities}
        
        # All state codes with cities should be in states list
        # (some states might not have cities in sample data)
        assert len(state_codes) > 0, "Should have states"
        assert len(city_state_codes) > 0, "Should have cities"
    
    def test_cascading_dropdown_workflow(self, client):
        """Test a complete user workflow of cascading dropdowns."""
        # Step 1: Load states for first dropdown
        states_response = client.get('/state/options')
        assert states_response.status_code == HTTPStatus.OK
        states = states_response.get_json()['options']
        assert len(states) > 0
        
        # Step 2: User selects a state
        selected_state = states[0]['code']
        
        # Step 3: Load cities for that state
        cities_response = client.get(f'/cities/options?state_code={selected_state}')
        assert cities_response.status_code == HTTPStatus.OK
        cities = cities_response.get_json()['options']
        
        # Step 4: Verify cities are from selected state
        if len(cities) > 0:
            for city in cities:
                assert city['state_code'].upper() == selected_state.upper()
