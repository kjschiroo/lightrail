# lightrail #

Module for monitoring twin cities lightrail

## install ##
    git clone https://github.com/kjschiroo/lightrail.git
    cd lightrail
    python3 setup.py install

## usage ##
List station codes

    python3 -m lightrail.cmdline -l

Monitor lightrail station

    python3 -m lightrail.cmdline [-x] [-b] <station_code>
