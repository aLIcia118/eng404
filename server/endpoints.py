"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus
import logging

from flask import Flask  # , request
from flask_restx import Resource, Api  # , fields  # Namespace
from flask_cors import CORS

# import werkzeug.exceptions as wz

import cities.queries as cqry

app = Flask(__name__)
CORS(app)
api = Api(app)

logging.basicConfig(
    level=logging.INFO,  # set to DEBUG for more detailed output
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

ERROR = 'Error'
MESSAGE = 'Message'
NUM_RECS = 'Number of Records'
READ = 'read'

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
MESSAGE = 'Message'

CITIES_EPS = '/cities'
CITY_RESP = 'Cities'
ENPOINT_RESP= 'Available endpoints'

@api.route(f'{CITIES_EPS}/{READ}')
class Cities(Resource):
    def get(self):
        try: 
            cities = cqry.read()
            num_recs = len(cities)
            log.info("Successfully fetched %d cities", num_recs)
            # success → 200
            return {CITY_RESP: cities, NUM_RECS: num_recs}, HTTPStatus.OK
        except ConnectionError as e:
            log.warning("Connection error in /cities/read: %s", e)
            # backend unavailable → 503
            return {ERROR: str(e)}, HTTPStatus.SERVICE_UNAVAILABLE
        print(f'{cities=}')
        return{
            CITY_RESP: cities,
            NUM_RECS: num_recs,
        }


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
        log.debug("Received request on /hello")
        return {HELLO_RESP: 'world'}, HTTPStatus.OK


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
        log.info("Listing %d endpoints", len(endpoints))
        return {"Available endpoints": endpoints}, HTTPStatus.OK
