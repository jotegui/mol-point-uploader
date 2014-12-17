__author__ = '@jotegui'

import os
from flask import Flask, session

#UPLOAD_FOLDER = '/home/jotegui/MapOfLife/PointUploader/loader_app/uploads/'

app = Flask(__name__)
app.config.from_object('config')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'

from loader_app import views, filters

app.jinja_env.filters['format_datetime'] = filters.filter_format_datetime
app.jinja_env.filters['format_timedelta'] = filters.filter_format_timedelta
