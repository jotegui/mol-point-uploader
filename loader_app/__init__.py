__author__ = '@jotegui'

import os
from flask import Flask, session

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'some_secret'

from loader_app import views, filters

app.jinja_env.filters['format_datetime'] = filters.filter_format_datetime
app.jinja_env.filters['format_timedelta'] = filters.filter_format_timedelta
