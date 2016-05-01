import urllib.request as request
from urllib.error import URLError
import json
from time import sleep


SOUTH = 1
EAST = 2
WEST = 3
NORTH = 4


PROVIDERS_URL = 'http://svc.metrotransit.org/NexTrip/Providers?format=json'
ROUTES_URL = 'http://svc.metrotransit.org/NexTrip/Routes?format=json'
DIRECTIONS_URL = 'http://svc.metrotransit.org/NexTrip/Directions/{route}?format=json'
STOPS_URL = 'http://svc.metrotransit.org/NexTrip/Stops/{route}/{direction}?format=json'
DEPARTURES_URL = 'http://svc.metrotransit.org/NexTrip/{stopid}?format=json'
TIMEPOINTDEPARTURES_URL = (
    'http://svc.metrotransit.org/NexTrip/{route}/{direction}/{stop}?format=json'
)
VEHICLELOCATIONS_URL = 'http://svc.metrotransit.org/NexTrip/VehicleLocations/{route}?format=json'


def _try_request_open(req, attempts=5):
    for i in range(attempts):
        try:
            response = request.urlopen(req)
            break
        except URLError as e:
            if i < attempts - 1:
                sleep(i)
                continue
            else:
                raise e
    return response


def _make_api_request(url):
    req = request.Request(url)
    response = _try_request_open(req).read()
    return json.loads(response.decode("utf8"))


def providers():
    url = PROVIDERS_URL
    return _make_api_request(url)


def routes():
    url = ROUTES_URL
    return _make_api_request(url)


def directions(route):
    url = DIRECTIONS_URL.format(route=route)
    return _make_api_request(url)


def stops(route, direction):
    url = STOPS_URL.format(route=route, direction=direction)
    return _make_api_request(url)


def departures(stopid):
    url = DEPARTURES_URL.format(stopid=stopid)
    return _make_api_request(url)


def timepointdepartures(route, direction, stop):
    url = TIMEPOINTDEPARTURES_URL.format(route=route,
                                         direction=direction,
                                         stop=stop)
    return _make_api_request(url)
