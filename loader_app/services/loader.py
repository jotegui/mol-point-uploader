import os
from urllib2 import urlopen
from urllib import urlencode
import json
import logging

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cdbkey.txt')
api_key = open(path, "r").read().rstrip()
url = "https://mol.cartodb.com/api/v2/sql"

def cdb(q):

    params = {'api_key':api_key, 'q':q}
    data = urlencode(params)
    raw = urlopen(url, data=data).read()
    d = json.loads(raw)
    return json.dumps(d)


def f(environ, start_response, q):

    status = '200'
    headers = []
    start_response(status, headers)

    d = cdb(q)
    return d


def species(environ, start_response):
	
    dId = environ['PATH_INFO'].split('/')[-1]
    q = "select distinct scientificname from point_uploads_master where datasetid='{0}'".format(dId)
    logging.info(q)
    d = f(environ, start_response, q)
    return d


def title(environ, start_response):

    dId = environ['PATH_INFO'].split('/')[-1]
    q = "select title from point_uploads_registry where datasetid='{0}'".format(dId)
    d = f(environ, start_response, q)
    return d


def mapAvailable(environ, start_response):

    dId = environ['PATH_INFO'].split('/')[-1]
    q = "select count(*)>0 as mapAvailable from point_uploads_master where datasetid='{0}'".format(dId)    
    d = f(environ, start_response, q)
    return d


def points(environ, start_response):

    dId = environ['PATH_INFO'].split('/')[-2]

    if dId == 'points':
        dId = environ['PATH_INFO'].split('/')[-1]
        selected = ''
    else:
        selected = environ['PATH_INFO'].split('/')[-1]
    
    q = "select scientificname, decimallatitude, decimallongitude, decimallatitude || ', ' || decimallongitude as coordinates, eventdate, recordedby, coordinateuncertaintyinmeters, geodeticdatum from point_uploads_master where datasetid='{0}'".format(dId)
    if selected != '':
        q += " and scientificname='{0}'".format(selected)
    logging.info(q)
    d = f(environ, start_response, q)
    return d