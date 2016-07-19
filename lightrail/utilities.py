from . import mtapi


GREENLINE = 902


def station_code_to_name_map():
    codes_to_station = {}
    station_to_codes = gather_station_codes()
    for station in station_to_codes:
        for code in station_to_codes[station]:
            codes_to_station[code] = station
    return codes_to_station


def gather_station_codes():
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


def get_soon_departures(station_code):
    soon_deps = []
    departures = mtapi.timepointdepartures(GREENLINE, mtapi.EAST, station_code)
    departures.extend(mtapi.timepointdepartures(GREENLINE, mtapi.WEST, station_code))
    for dep in departures:
        if 'Min' in dep['DepartureText'] or 'Due' in dep['DepartureText']:
            soon_deps.append({'time': dep['DepartureText'],
                              'direction': dep['RouteDirection']})
    return soon_deps
