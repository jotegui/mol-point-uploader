__author__ = '@jotegui'

import requests
import json
import os
import csv
import uuid
from StringIO import StringIO
from zipfile import ZipFile

from loader_app import app
from cartodb_apikey import api_key
from flask import session, flash

from google.appengine.ext import ndb
from Models import UploadedFile
from google.appengine.ext import blobstore

ALLOWED_EXTENSIONS = set(['txt','csv','tsv'])

class Uploader():
    """Several uploading methods."""

    def __init__(self):
        """Initialize the class and create storage for errors and warnings."""
        self.dataset_uuid = session['file_uuid']
        self.cartodb_api = 'https://mol.cartodb.com/api/v2/sql'
        self.any_error = False
        
        return

    
    def upload_ndb(self, name, content):
        """Upload the content of a file to the NDB datastore. Returns urlsafe entity key."""
        uploaded_file = UploadedFile(uuid=session['file_uuid'], name=name, content=str(content))
        file_key = uploaded_file.put().urlsafe()
        return file_key
    
    
    def parse_file(self, up_file):
        """Validate the file."""

        # Check for allowed file extension
        allowed_file = '.' in up_file.filename and up_file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        if allowed_file is False:
            flash("ERROR: Unsupported file type. File should be .txt, .csv or .tsv")
            self.any_error = True
            return
        
        # Check field separator
        headerline = up_file.readline().rstrip()
        if len(headerline.split(",")) > 1:
            session['field_separator'] = ","
        elif len(headerline.split("\t")) > 1:
            session['field_separator'] = "\t"
        elif len(headerline.split("|")) > 1:
            session['field_separator'] = "|"
        else:
            flash("ERROR: Unsupported field separator. Fields should be separated by comma (,), pipe (|) or tab")
            self.any_error = True
            return
        
        # Store headers
        session.pop('file_headers', None)
        session['file_headers'] = headerline.split(session['field_separator'])
        
        # Remove trailing newline
        content = up_file.read()
        if content[-1] == "\n":
            content = content[:-1]
        
        # Save the file to NDB
        session['raw_key'] = self.upload_ndb(name='raw', content=content)
        
        return
    
    
    def upload_meta(self, meta):
        """Upload the metafile to NDB Datastore."""
        session['meta_key'] = self.upload_ndb(name='meta', content=meta)
        return
    
    
    def upload_eml(self, eml):
        """Upload the eml metadata file to NDB Datastore."""
        session['eml_key'] = self.upload_ndb(name='eml', content=eml)
        return
    
    
    def build_occurrence(self):
        """Iterate through all records to build occurrence.txt"""
        blob = ndb.Key(urlsafe=session['raw_key']).get().content
        csvreader = csv.reader(blob.split("\n"), delimiter=str(session['field_separator']), quotechar='"')
        occurrence = ""
        for record in csvreader:
            row = self.line_dwca(record)
            occurrence += row
        if occurrence[-1] == "\n":
            occurrence = occurrence[:-1]
        session['occurrence_key'] = self.upload_ndb(name='occurrence', content=occurrence)
        return
        
        
    def line_dwca(self, record):
        """Prepare a line for the DWCA with the parsed record."""
        field_separator = "\t"
        row_separator = "\n"
        record_uuid = str(uuid.uuid4())
        dwc_record = [record[x] for x in session['dwc_headers']]
        row = field_separator.join([record_uuid, self.dataset_uuid, 'HumanObservation']+dwc_record)+row_separator
        return row
    
    
    def build_dwca(self):
        """Build the DarwinCore Archive and upload it to NDB Datastore."""
        
        # Get each file as a StringIO instance
        meta = ndb.Key(urlsafe=session['meta_key']).get().content
        eml = ndb.Key(urlsafe=session['eml_key']).get().content
        occurrence = ndb.Key(urlsafe=session['occurrence_key']).get().content
        
        # Create the DWCA as a ZipFile based on a StringIO instance
        dwca_s = StringIO()
        dwca = ZipFile(dwca_s, 'w')
        
        # Fill in all the files
        dwca.writestr('meta.xml', meta)
        dwca.writestr('eml.xml', eml)
        dwca.writestr('occurrence.txt', occurrence)
        
#        # Store it in Blobstore
#        upload_url = blobstore.create_upload_url('/upload_dwca')
#        params={'file':dwca, 'enctype':'multipart/form-data'}
#        r = requests.post(upload_url, params=params)
#        print r.status_code
#        print r.text
#        
#        # Store it in NDB Datastore
#        self.upload_ndb(name='dwca', content=dwca)
        
        # Close ZipFile and StringIO
        dwca.close()
        dwca_s.close()
        
        return
    
    
    def build_cartodb(self):
        """Iterate through all records to build the records to upoad to CartoDB"""
        
        table_name = 'point_uploads'

        # Open raw data file
        blob = ndb.Key(urlsafe=session['raw_key']).get().content
        
        # and for each record
        csvreader = csv.reader(blob.split("\n"), delimiter=str(session['field_separator']), quotechar='"')

        query_base = "insert into {0} (datasetId, scientificName, decimalLatitude, decimalLongitude, eventDate, recordedBy, extraFields, the_geom, the_geom_webmercator) values ".format(table_name)
        values = []
        for record in csvreader:
            value = self.add_record_to_cartodb(record, table_name)
            if value:
                values.append(value)
        
        # All at once
        query = query_base + ", ".join(values)
        print "Inserting {0} records".format(len(values))
        params = {'q': query, 'api_key': api_key}
        r = requests.post(self.cartodb_api, data=params)
        if r.status_code == 200:
            flash('File uploaded successfuly!'.format(table_name))
        else:
            flash('ERROR: something went wrong with the upload.')
            flash(r.text)
            flash('Please, fix the issue and try uploading again.')
        
        return
    
    
    def add_record_to_cartodb(self, record, table_name):
        """Prepare and upload the record to the new cartodb table."""
        
        # Locate mandatory fields
        for i in session['alignment']:
            if session['alignment'][i] == 'scientificName':
                scientificName_idx = session['file_headers'].index(i)
            elif session['alignment'][i] == 'decimalLatitude':
                decimalLatitude_idx = session['file_headers'].index(i)
            elif session['alignment'][i] == 'decimalLongitude':
                decimalLongitude_idx = session['file_headers'].index(i)
            elif session['alignment'][i] == 'eventDate':
                eventDate_idx = session['file_headers'].index(i)
            elif session['alignment'][i] == 'recordedBy':
                recordedBy_idx = session['file_headers'].index(i)
        
        # Populate mandatory variables
        datasetId = session['file_uuid']
        scientificName = record[scientificName_idx].replace('"','').replace("'", "")
        decimalLatitude = record[decimalLatitude_idx]
        decimalLongitude = record[decimalLongitude_idx]
        eventDate = record[eventDate_idx].replace('"','').replace("'", "")
        recordedBy = record[recordedBy_idx].replace('"','').replace("'", "")
        
        # Populate extraFields
        extraFields = {}
        for i in session['file_headers']:
            if i not in session['alignment']:
                idx = session['file_headers'].index(i)
                key = i
                value = record[idx].replace('"','').replace("'", "")
                extraFields[key] = value
        
        # Build query
        values = "('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', ST_SetSRID(ST_Point({3}, {2}),4326), ST_SetSRID(ST_Point({3}, {2}),3857))".format(datasetId, scientificName, decimalLatitude, decimalLongitude, eventDate, recordedBy, json.dumps(extraFields))
        
        return values
