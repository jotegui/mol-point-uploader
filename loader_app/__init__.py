__author__ = '@jotegui'

import os
from flask import Flask, session

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'some_secret'

import loader_app.views
