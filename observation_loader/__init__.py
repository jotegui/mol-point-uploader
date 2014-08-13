import os
from flask import Flask, session


UPLOAD_FOLDER = '/home/jotegui/MapOfLife/PointUploader/observation_loader/uploads/' # TODO: update

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'some_secret'

import observation_loader.views
