"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
from pathlib import Path

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS

from data.db_connect import connect_db
from data.db_connect import ensure_indexes
from data.samples import (
    SAMPLE_CITIES_LIST,
    SAMPLE_CITIES_DICT,
    SAMPLE_STATES,
)

import cities.queries as cqry
import USstates.queries as sqry

app = Flask(__name__)
CORS(app)
api = Api(app)
ensure_indexes()

ERROR = 'Error'
MESSAGE = 'Message'
NUM_RECS = 'Number of Records'
READ = 'read'

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'

STATES_EPS = '/state'
STATE_RESP = 'States'

HELLO_EP = '/hello'
HELLO_RESP = 'hello'

CITIES_EPS = '/cities'
CITY_RESP = 'Cities'

HEALTH_DB_EP = "/health/db"
DEVELOPER_LOGS_EP = "/developer/logs"

# HATEOAS dropdown options endpoints
STATE_OPTIONS_EP = '/state/options'
CITY_OPTIONS_EP = '/cities/options'

DEFAULT_LOG_PATHS = (
    Path("/var/log/emu86.pythonanywhere.com.server.log"),
    Path("/var/log/emu86.pythonanywhere.com.error.log"),
    Path("/var/log/emu86.pythonanywhere.com.access.log"),
)


def _tail_lines(log_path: Path, lines: int) -> list[str]:
    with log_path.open("r", encoding="utf-8", errors="replace") as handle:
        contents = handle.readlines()
    return [line.rstrip("\n") for line in contents[-lines:]]

# Swagger / RESTX model describing the JSON body for a city
city_model = api.model(
    "City",
    {
        "name": fields.String(required=True, description="City name"),
        "state_code": fields.String(required=True, description="2-letter state code"),
    },
)

@api.route(f"{STATES_EPS}/<string:state_code>")
class StateDetail(Resource):
    """
    Get a single state by its postal code, e.g. /state/NY.
    """
    def get(self, state_code: str):
        try:
            states_data = sqry.read()
        except ConnectionError as e:
            return {ERROR: str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

        code = state_code.upper()
        rec = None

        if isinstance(states_data, dict):
            rec = states_data.get(code)
        else:
            for s in states_data:
                if str(s.get("code", "")).upper() == code:
                    rec = s
                    break

        if rec is None:
            return {ERROR: f"State not found: {code}"}, HTTPStatus.NOT_FOUND

        return rec, HTTPStatus.OK


@api.route(f"{STATES_EPS}/{READ}")
class States(Resource):
    """
    Endpoint to list all US states.
    """
    def get(self):
        """
        Return all states and a count of records.
        """
        
        try:
            # Assuming sqry.read() returns a dict of states or a list
            states_data = sqry.read()
            # If it's a dict, get its length via len(states_data)
            num_recs = len(states_data)
            # Use sample data if database is empty
            if not states_data or num_recs == 0:
                states_data = SAMPLE_STATES
                num_recs = len(states_data)
        except (ConnectionError, Exception):
            # Use sample data if database connection fails
            states_data = SAMPLE_STATES
            num_recs = len(states_data)

        return {
            STATE_RESP: states_data,
            NUM_RECS: num_recs,
        }, HTTPStatus.OK

@api.route(f'{CITIES_EPS}/{READ}')
class Cities(Resource):
    """
    Return all cities and a count of records.
    """
    def get(self):
        """
        Return all cities and a count of records.
        """
        try:
            cities = cqry.read()
            num_recs = len(cities)
        except (ConnectionError, Exception):
            cities = SAMPLE_CITIES_LIST
            num_recs = len(cities)
        
        # Use sample data if database returned empty
        if not cities or num_recs == 0:
            cities = SAMPLE_CITIES_LIST
            num_recs = len(cities)
        
        return {
            CITY_RESP: cities,
            NUM_RECS: num_recs,
        }, HTTPStatus.OK

@api.route(CITIES_EPS)
class CitiesList(Resource):
    """
    List all cities or create a new city.
    """
    
    def get(self):
        """
        Return a list of all cities.
        """
        state_code = request.args.get("state_code")
        limit_str = request.args.get("limit")
        try:
            cities_dict = cqry.read()
        except (ConnectionError, Exception):
            cities_dict = SAMPLE_CITIES_DICT
        
        # Use sample data if database returned empty
        if not cities_dict:
            cities_dict = SAMPLE_CITIES_DICT

        cities_list = list(cities_dict.values())
        if state_code:
            code_upper = state_code.upper()
            cities_list = [
                c for c in cities_list
                if c.get("state_code", "").upper() == code_upper
            ]
        if limit_str:
            try:
                limit = int(limit_str)
                if limit > 0:
                    cities_list = cities_list[:limit]
            except ValueError:
                pass

        return cities_list, HTTPStatus.OK

    def post(self):
        """
        Create a new city.
        Expects JSON: { "name": "...", "state_code": "..." }
        """
        data = request.get_json() or {}
        # data = api.payload or {}
        try:
            new_id = cqry.create(data)
            rec = cqry.read_one(new_id)
        except ValueError as e:
            return {ERROR: str(e)}, HTTPStatus.BAD_REQUEST

        return rec, HTTPStatus.CREATED

@api.route(f"{CITIES_EPS}/<string:city_id>")
class CityDetail(Resource):
    """
    Get, update, or delete a single city by its internal ID.
    """

    def get(self, city_id: str):
        rec = cqry.read_one(city_id)
        if rec is None:
            return {ERROR: f"City not found: {city_id}"}, HTTPStatus.NOT_FOUND
        return rec, HTTPStatus.OK

    def patch(self, city_id: str):
        """
        Partially update a city.
        """
        updates = request.get_json() or {}
        try:
            updated = cqry.update(city_id, updates)
        except ValueError as e:
            # invalid id or city not found
            return {ERROR: str(e)}, HTTPStatus.BAD_REQUEST
        return updated, HTTPStatus.OK

    def delete(self, city_id: str):
        """
        Delete a city by id.
        """
        try:
            ok = cqry.delete(city_id)
        except ValueError as e:
            return {ERROR: str(e)}, HTTPStatus.NOT_FOUND

        if ok:
            return {}, HTTPStatus.NO_CONTENT
        return {ERROR: "Delete failed"}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route(STATE_OPTIONS_EP)
class StateOptions(Resource):
    """
    HATEOAS endpoint that returns state options for dropdown menus.
    Returns list of state objects with code and name.
    """
    SAMPLE_STATE_OPTIONS = [
        {"code": "NY", "name": "New York"},
        {"code": "CA", "name": "California"},
        {"code": "TX", "name": "Texas"},
        {"code": "FL", "name": "Florida"},
        {"code": "PA", "name": "Pennsylvania"},
        {"code": "IL", "name": "Illinois"},
        {"code": "OH", "name": "Ohio"},
        {"code": "GA", "name": "Georgia"},
        {"code": "NC", "name": "North Carolina"},
        {"code": "MI", "name": "Michigan"},
    ]
    
    def get(self):
        """
        Return available states for dropdown selection.
        """
        try:
            states_data = sqry.read()
            # Transform to dropdown format if needed
            if isinstance(states_data, dict):
                options = [
                    {"code": code, "name": state.get("name", code)} 
                    for code, state in states_data.items()
                ]
            else:
                options = [
                    {"code": s.get("code", ""), "name": s.get("name", "")} 
                    for s in states_data
                ]
        except (ConnectionError, Exception):
            options = self.SAMPLE_STATE_OPTIONS
        
        if not options:
            options = self.SAMPLE_STATE_OPTIONS
        
        enriched_options = [
            {
                **option,
                "links": {
                    "self": f"{STATE_OPTIONS_EP}?code={option['code']}",
                    "cities": f"{CITY_OPTIONS_EP}?state_code={option['code']}",
                    "state_detail": f"{STATES_EPS}/{option['code']}",
                },
            }
            for option in options
        ]

        return {
            "options": enriched_options,
            "links": {
                "self": STATE_OPTIONS_EP,
            },
        }, HTTPStatus.OK

@api.route(CITY_OPTIONS_EP)
class CityOptions(Resource):
    """
    HATEOAS endpoint that returns city options for dropdown menus.
    Can filter by state_code query parameter.
    """
    SAMPLE_CITY_OPTIONS = [
        {"id": "NYC001", "name": "New York", "state_code": "NY"},
        {"id": "NYC002", "name": "Buffalo", "state_code": "NY"},
        {"id": "NYC003", "name": "Rochester", "state_code": "NY"},
        {"id": "LAC001", "name": "Los Angeles", "state_code": "CA"},
        {"id": "LAC002", "name": "San Francisco", "state_code": "CA"},
        {"id": "LAC003", "name": "San Diego", "state_code": "CA"},
        {"id": "TXC001", "name": "Houston", "state_code": "TX"},
        {"id": "TXC002", "name": "Dallas", "state_code": "TX"},
        {"id": "TXC003", "name": "Austin", "state_code": "TX"},
    ]
    
    def get(self):
        """
        Return available cities for dropdown selection.
        Optional query parameter: state_code (e.g., ?state_code=NY)
        """
        state_code = request.args.get("state_code")
        
        try:
            cities_dict = cqry.read()
            # Transform to dropdown format
            options = [
                {
                    "id": city.get("id") or city.get("_id", ""),
                    "name": city.get("name", ""),
                    "state_code": city.get("state_code", ""),
                }
                for city in cities_dict.values()
            ]
        except (ConnectionError, Exception):
            options = self.SAMPLE_CITY_OPTIONS
        
        if not options:
            options = self.SAMPLE_CITY_OPTIONS
        
        # Filter by state if provided
        if state_code:
            code_upper = state_code.upper()
            options = [
                c for c in options 
                if c.get("state_code", "").upper() == code_upper
            ]
        
        enriched_options = [
            {
                **option,
                "links": {
                    "self": f"{CITIES_EPS}/{option['id']}",
                    "collection": CITIES_EPS,
                    "state_options": f"{STATE_OPTIONS_EP}",
                },
            }
            for option in options
        ]

        collection_link = CITY_OPTIONS_EP
        if state_code:
            collection_link = f"{CITY_OPTIONS_EP}?state_code={state_code.upper()}"

        return {
            "options": enriched_options,
            "links": {
                "self": collection_link,
                "state_options": STATE_OPTIONS_EP,
            },
        }, HTTPStatus.OK

@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {HELLO_RESP: 'world'}, HTTPStatus.OK

@api.route(HEALTH_DB_EP)
class HealthDB(Resource):
    """
    Endpoint to verify MongoDB connectivity.
    """
    def get(self):
        try:
            client = connect_db()
            client.admin.command("ping")
            return {"ok": True, "message": "Mongo reachable"}
        except Exception as e:
            return {"ok": False, "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR


@api.route(DEVELOPER_LOGS_EP)
class DeveloperLogs(Resource):
    """
    Developer-facing endpoint for inspecting recent application logs.
    """

    def get(self):
        requested_path = request.args.get("path")
        limit_arg = request.args.get("lines", "50")

        try:
            line_limit = max(1, min(int(limit_arg), 200))
        except ValueError:
            return {ERROR: "lines must be an integer between 1 and 200"}, HTTPStatus.BAD_REQUEST

        if requested_path:
            log_path = Path(requested_path)
        else:
            available_paths = [path for path in DEFAULT_LOG_PATHS if path.exists()]
            if not available_paths:
                return {
                    MESSAGE: "No configured log files were found",
                    "candidates": [str(path) for path in DEFAULT_LOG_PATHS],
                }, HTTPStatus.NOT_FOUND
            log_path = available_paths[0]

        if not log_path.exists() or not log_path.is_file():
            return {ERROR: f"Log file not found: {log_path}"}, HTTPStatus.NOT_FOUND

        try:
            log_lines = _tail_lines(log_path, line_limit)
        except OSError as exc:
            return {ERROR: f"Unable to read log file: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {
            "path": str(log_path),
            "lines_requested": line_limit,
            "lines": log_lines,
        }, HTTPStatus.OK

@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        # return {"Available endpoints": endpoints}
        return {ENDPOINT_RESP: endpoints}, HTTPStatus.OK
