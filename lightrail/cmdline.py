"""cmdline

Usage:
    cmdline [-b] [-x] <station_code>
    cmdline -l
    cmdline (-h | --help)
Options:
    -b                 Big text
    -x                 Expand station code to name
"""
from docopt import docopt
from pyfiglet import Figlet
from . import mtapi
import os
from time import sleep
import sys


GREENLINE = 902


def _station_code_to_name_map():
    codes_to_station = {}
    station_to_codes = _gather_station_codes()
    for station in station_to_codes:
        for code in station_to_codes[station]:
            codes_to_station[code] = station
    return codes_to_station


def _gather_station_codes():
    stations = {}
    for d in [mtapi.EAST, mtapi.WEST]:
        results = mtapi.stops(GREENLINE, d)
        for r in results:
            st_name = r['Text'].strip()
            st_code = r['Value']
            if st_name not in stations:
                stations[st_name] = []
            if st_code not in stations[st_name]:
                stations[st_name].append(st_code)
    return stations


def list_station_codes():
    column1 = '{0}: '
    stations = _gather_station_codes()
    keys = stations.keys()
    for key in sorted(keys):
        print(column1.format(key) + ', '.join(stations[key]))


def _get_soon_departures(station_code):
    soon_deps = []
    departures = mtapi.timepointdepartures(GREENLINE, mtapi.EAST, station_code)
    departures.extend(mtapi.timepointdepartures(GREENLINE, mtapi.WEST, station_code))
    for dep in departures:
        if 'Min' in dep['DepartureText'] or 'Due' in dep['DepartureText']:
            soon_deps.append({'time': dep['DepartureText'],
                              'direction': dep['RouteDirection']})
    return soon_deps


def _prepare_departure_text(departures):
    row_format = '{0} - {1}'
    rows = [row_format.format(d['direction'][0], d['time']) for d in departures]
    return '\n'.join(rows)


def _print_text(text, big):
    if big:
        text_renderer = Figlet(font='standard', width=180)
        text = text_renderer.renderText(text)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(text)


def _waiting_bar(wait_time):
    for i in range(wait_time):
        sleep(1)
        print(' ', end='')
        sys.stdout.flush()
    print()


def display_station(station_code, big, expand):
    printed_name = station_code
    codes = _station_code_to_name_map()
    if station_code not in codes:
        print("{0} not a known station code".format(station_code))
        return
    if expand:
        printed_name = codes[station_code]
    while(True):
        departures = _get_soon_departures(station_code)
        dep_text = _prepare_departure_text(departures)
        text = printed_name + '\n' + dep_text
        _print_text(text, big)
        _waiting_bar(30)


def main(args):
    if args['-l']:
        list_station_codes()
    elif args['<station_code>'] is not None:
        display_station(args['<station_code>'].upper(), args['-b'], args['-x'])


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)
