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
from flask import session, flash, g, render_template

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
        self.namedmaps_api = 'https://mol.cartodb.com/api/v1/map/named'
        self.template_id = 'mol@mol_pointupload'
        self.any_error = False
        
        return

    
    # NDB entity operations
    
    
    def upload_ndb(self, name, content):
        """Upload the content of a file to the NDB datastore. Returns urlsafe entity key."""
        uploaded_file = UploadedFile(uuid=session['file_uuid'], name=name, content=str(content))
        file_key = uploaded_file.put().urlsafe()
        return file_key
    
    
    def delete_entity(self, key_name):
        """Delete a single entity from the NDB datastore."""
        ndb.Key(urlsafe = session[key_name]).delete()
        return
    
    
    def delete_ndb(self):
        """Delete all stored entities from NDB Datastore."""
        for key in ['raw_key', 'meta_key', 'eml_key', 'occurrence_key']:
            self.delete_entity(key)
        return
    
    
    def parse_file(self, up_file):
        """Validate the uploaded file."""

        # Check for allowed file extension
        allowed_file = '.' in up_file.filename and up_file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        if allowed_file is False:
            flash("ERROR: Unsupported file type. File should be .txt, .csv or .tsv")
            self.any_error = True
            return
        
        # Check field separator
        headerline = up_file.readline().rstrip().decode('utf-8')
        if len(headerline.split(",")) > 1:
            session['field_separator'] = ","
        elif len(headerline.split(";")) > 1:
            session['field_separator'] = ";"
        elif len(headerline.split("\t")) > 1:
            session['field_separator'] = "\t"
        elif len(headerline.split("|")) > 1:
            session['field_separator'] = "|"
        else:
            flash("ERROR: Unsupported field separator. Fields should be separated by comma (,), semicolon (;), pipe (|) or tab")
            self.any_error = True
            return
        
        # Store headers
        session.pop('file_headers', None)
        session['file_headers'] = headerline.split(session['field_separator'])
        
        # Read file into unicode
        content = up_file.read()

        # Remove trailing newline
        if content[-1] == "\n":
            content = content[:-1]
        
        # Save the file to NDB
        session['raw_key'] = str(self.upload_ndb(name='raw', content=content))
        print 'raw_key = {0}'.format(session['raw_key'])
        
        return
    
    
    def upload_meta(self, meta):
        """Upload the metafile to NDB Datastore."""
        session['meta_key'] = self.upload_ndb(name='meta', content=meta)
        print 'meta_key = {0}'.format(session['meta_key'])
        return
    
    
    def upload_eml(self, eml):
        """Upload the eml metadata file to NDB Datastore."""
        session['eml_key'] = self.upload_ndb(name='eml', content=eml)
        print 'eml_key = {0}'.format(session['eml_key'])
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
        print 'occurrence_key = {0}'.format(session['occurrence_key'])
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
    
    
    def cartodb_meta(self, request):
        """Build and insert the record to the CartoDB point uploads registry."""
        
        table_name = 'point_uploads_registry'
        
        # Get user from auth
        user = g.get('user', None)
        userEmail = user['email']
        
        # Populate fields
        datasetId = session['file_uuid']
        public = True if 'public' in request.keys() and request['public'] == 'on' else False
        title = request['title'].replace("'", "''").encode('utf-8')
        abstract = request['abstract'].replace("'", "''").encode('utf-8')
        creatorEmail = request['resource_creator_email'].replace("'", "''").encode('utf-8')
        creatorFirst = request['resource_creator_first_name'].replace("'", "''").encode('utf-8')
        creatorLast = request['resource_creator_last_name'].replace("'", "''").encode('utf-8')
        metadataEmail = request['metadata_creator_email'].replace("'", "''").encode('utf-8')
        metadataFirst = request['metadata_creator_first_name'].replace("'", "''").encode('utf-8')
        metadataLast = request['metadata_creator_last_name'].replace("'", "''").encode('utf-8')
        lang = request['lang'].replace("'", "''").encode('utf-8') if 'lang' in request and request['lang'] != "" else 'en'
        geographicScope = request['geographic_scope'].replace("'", "''").encode('utf-8')
        temporalScope = request['temporal_scope'].replace("'", "''").encode('utf-8')
        taxonomicScope = request['taxonomic_scope'].replace("'", "''").encode('utf-8')
        keywords = json.dumps([x.strip() for x in request['keywords'].split(';')], ensure_ascii=False).replace('[','{').replace(']','}').encode('utf-8')
        license = request['license'].replace("'", "''").encode('utf-8')
        additionalInformation = request['additional_information'].replace("'", "''").encode('utf-8')
        
        # Build extrafields with the description and headers of non-mandatory fields
        extrafields = {}
        for i in session['extra_fields']:
            dic = {}
            for j in session['extra_fields'][i]:
                dic[j] = session['extra_fields'][i][j]
            extrafields[i.encode('utf-8')] = dic
        extrafields = unicode(json.dumps(extrafields), 'utf-8')
        
        query = unicode("insert into {0} (datasetId, public, title, abstract, creatorEmail, creatorFirst, creatorLast, metadataEmail, metadataFirst, metadataLast, lang, geographicScope, temporalScope, taxonomicScope, keywords, license, additionalInformation, extrafields, email) values ('{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}', '{18}', '{19}')".format(table_name, datasetId, public, title, abstract, creatorEmail, creatorFirst, creatorLast, metadataEmail, metadataFirst, metadataLast, lang, geographicScope, temporalScope, taxonomicScope, keywords, license, additionalInformation, extrafields, userEmail), 'utf-8')
        
        params = {'q': query, 'api_key': api_key}
        r = requests.post(self.cartodb_api, data=params)

        if r.status_code == 200:
            print 'Registry entry added'
        else:
            print 'Something went wrong:'
            print r.status_code
            print r.text
        
        return
    
    def cartodb_points(self):
        """Iterate through all records to build the records to upoad to CartoDB"""
        
        table_name = 'point_uploads'
        
        # Open raw data file
        blob = ndb.Key(urlsafe=session['raw_key']).get().content
        
        # and for each record
        csvreader = csv.reader(blob.split("\n"), delimiter=str(session['field_separator']), quotechar='"')

        query_base = "insert into {0} (datasetId, scientificName, decimalLatitude, decimalLongitude, eventDate, recordedBy, extraFields, the_geom, the_geom_webmercator) values ".format(table_name)
        values = []
        for record in csvreader:
            print record
            value = self.add_record_to_query([unicode(x, 'utf-8', errors="ignore") for x in record])
            if value:
                values.append(value)
        
        # All at once
        query = query_base + ", ".join(values)
        print "Inserting {0} records".format(len(values))
        params = {'q': query, 'api_key': api_key}
        r = requests.post(self.cartodb_api, data=params)
        if r.status_code == 200:
            flash('File uploaded successfuly!')
        else:
            flash('ERROR: something went wrong with the upload.')
            flash(r.text)
            flash('Please, fix the issue and try uploading again.')
        
        return
    
    
    def add_record_to_query(self, record):
        """Prepare and upload the record to the new cartodb table."""

        # Find and populate mandatory variables        
        datasetId = session['file_uuid']
        
        # Container for record values
        vals = {}
        
        # For each mandatory header
        for i in session['headers']:
            
            # DarwinCore name for the header
            dwc_header = i
            
            # Name of the header as it appears in the file, or None if default is to be applied
            file_header = session['headers'][i] if session['headers'][i] != '' else None
            
            # If header is not in file, apply default value
            if file_header is None:
                vals[i] = session['defaults'][i]
            
            # If header is in file
            else:
                
                # Grab value record in correspondent position
                idx = session['file_headers'].index(file_header) if file_header is not None else None
                val = record[idx].replace('"','').replace("'", "")

                # If value is missing, apply default value
                if val == '':
                    val = session['defaults'][i]
                
                # Store value in container
                vals[i] = val.encode('utf-8')

        # Populate extraFields
        extraFields = {}
        for i in session['file_headers']:
            if i not in session['headers'].values():
                idx = session['file_headers'].index(i)
                key = i
                value = record[idx].replace('"','').replace("'", "")
                extraFields[key] = value
        
        
        # Build geom fields
        try:
           latval = float(vals['decimalLatitude'])
           lngval = float(vals['decimalLongitude'])
           geoms = "ST_SetSRID(ST_Point({0}, {1}),4326), ST_SetSRID(ST_Point({0}, {1}),3857)".format(vals['decimalLongitude'], vals['decimalLatitude'])
        except ValueError:
            geoms = "null, null"

        # Change some empty values for nulls
        if vals['decimalLatitude'] == '':
            vals['decimalLatitude'] = 'null'
        if vals['decimalLongitude'] == '':
            vals['decimalLongitude'] = 'null'
        
        # Build record for query
        values = unicode("('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', {7})".format(datasetId, vals['scientificName'], vals['decimalLatitude'], vals['decimalLongitude'], vals['eventDate'], vals['recordedBy'], json.dumps(extraFields), geoms), 'utf-8')
        print values
        return values


#    def cdb_instantiate_named_map(self):
#        """Instantiate a named map with the contents of the dataset."""
#        
#        params = {"api_key": api_key}
#        params_json = json.dumps({"datasetid": self.dataset_uuid})
#        url = self.namedmaps_api+"/"+self.template_id

#        r = requests.post(url, params=params, data=params_json, headers={"content-type":"application/json"})

#        if r.status_code == 200:
#            self.layergroupid = r.json()['layergroupid']
#        else:
#            self.layergroupid = None
#        print self.layergroupid
#        
#        return
