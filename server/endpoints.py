"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

#test: trigger CI run
from http import HTTPStatus

from flask import Flask, request
# from flask_restx import Resource, Api  # , fields  # Namespace
from flask_restx import Resource, Api, fields  # Namespace
from flask_cors import CORS

from data.db_connect import connect_db

from data.db_connect import ensure_indexes

# import werkzeug.exceptions as wz

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
        else: we talk about
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
        except ConnectionError as e:
            return {ERROR: str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {
            STATE_RESP: states_data,
            NUM_RECS: num_recs,
        }, HTTPStatus.OK

@api.route(f'{CITIES_EPS}/{READ}')
class Cities(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        try:
            cities = cqry.read()
            num_recs = len(cities)
        except ConnectionError as e:
            return {ERROR: str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
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
        except ConnectionError:
            return [], HTTPStatus.OK

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
