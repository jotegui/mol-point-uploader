__author__ = '@jotegui'

import os
from flask import Flask, session

#UPLOAD_FOLDER = '/home/jotegui/MapOfLife/PointUploader/loader_app/uploads/'

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'

import loader_app.views
