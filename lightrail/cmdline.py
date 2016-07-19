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
from . import utilities as utils
import os
from time import sleep
import sys


def list_station_codes():
    column1 = '{0}: '
    stations = utils.gather_station_codes()
    keys = stations.keys()
    for key in sorted(keys):
        print(column1.format(key) + ', '.join(stations[key]))


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
    codes = utils.station_code_to_name_map()
    if station_code not in codes:
        print("{0} not a known station code".format(station_code))
        return
    if expand:
        printed_name = codes[station_code]
    while(True):
        departures = utils.get_soon_departures(station_code)
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
