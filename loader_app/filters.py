""" Application template filters"""

__author__ = 'funkycoda'

import urllib
from datetime import datetime, time
from dateutil.parser import parse

from babel.dates import format_date, format_datetime, format_time, timedelta, format_timedelta


def filter_format_datetime(value):
    dt = parse(value)
    dts = format_datetime(dt, format='medium', locale='en')
    return dts


def filter_format_timedelta(value):
    dt = parse(value)
    dts = format_timedelta(dt - datetime.now(dt.tzinfo), format='medium', locale='en')

    return dts


def filter_obscode(value):
    if value == 1:
        return '100m'
    elif value == 2:
        return '5km'
    return 'none'


def filter_unescapetext(value):
    print("Value 1: " + value)
    print("Value 2: " + urllib.unquote(value))
    #return urllib.unquote(value)
    return value.replace('&#34;', '"')
    #return value.replace('50000', 'fiver')


