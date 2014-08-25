from observation_loader import app
from cartodb_apikey import api_key
from flask import session, flash
import requests
import json
import os
import csv
import uuid

class Uploader():


    def __init__(self):
        """Initialize the class and create storage for errors and warnings."""
        self.dataset_uuid = session['file_uuid']
        self.cartodb_api = 'https://mol.cartodb.com/api/v2/sql'


    def build_occurrence(self):
        """Iterate through all records to build occurrence.txt"""
        with open(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "raw.csv"), 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=session['field_separator'], quotechar='"')
            for record in csvreader:
                self.add_record_to_dwca(record)
        return
        
        
    def add_record_to_dwca(self, record):
        """Open the occurrence.txt file and add the parsed record."""
        field_separator = "\t"
        row_separator = "\n"
        record_uuid = str(uuid.uuid4())
        dwc_record = [record[x] for x in session['dwc_headers']]
        row = field_separator.join([record_uuid, self.dataset_uuid, 'HumanObservation']+dwc_record)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], self.dataset_uuid, "occurrence.txt"), 'a') as w:
            w.write(row)
            w.write(row_separator)
    
    
    def build_cartodb(self):
        """Iterate through all records to build the records to upoad to CartoDB"""
        
        # Create table
        table_name = 'points_{0}'.format(session['file_uuid'].replace('-','_'))
        query = "create table {0}(cartodb_id serial not null primary key, datasetId varchar(36), scientificName text, decimalLatitude float, decimalLongitude float, eventDate text, recordedBy text, extraFields json)".format(table_name)
        params = {'q': query, 'api_key': api_key}
        r = requests.get(self.cartodb_api, params=params)
        
        # If successful
        if r.status_code == 200:
            print 'Table {0} was created'.format(table_name)
            
            # Open raw data file
            with open(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "raw.csv"), 'rb') as csvfile:
                # and for each record
                csvreader = csv.reader(csvfile, delimiter=session['field_separator'], quotechar='"')

                query_base = "insert into {0} (datasetId, scientificName, decimalLatitude, decimalLongitude, eventDate, recordedBy, extraFields) values ".format(table_name)
                values = []
                for record in csvreader:
                    #cont += 1
                    # add it to the new table
                    #r_ins = self.add_record_to_cartodb(record, table_name)
                    #if r_ins.status_code == 200:
                    #    print 'Record {0} was inserted'.format(cont)
                    #else:
                    #    print 'Something went wrong inserting record {0}:\n{1}'.format(cont, r_ins.text)
                    value = self.add_record_to_cartodb(record, table_name)
                    if value:
                        values.append(value)
                
                # All at once
                query = query_base + ", ".join(values)
                print "Inserting {0} records".format(len(values))
                params = {'q': query, 'api_key': api_key}
                r = requests.post(self.cartodb_api, data=params)
                print r.status_code
                print r.text
                if r.status_code == 200:
                    flash('File uploaded successfuly!')
                else:
                    flash('ERROR: something went wrong with the upload.')
                    flash(r.text)
                    flash('Please, fix the issue and try uploading again.')
                
#                # In 100 record chunks
#                # Split in chunks of 100
#                cont = 0
#                max=100
#                
#                # Initialize
#                chunk = values[cont:cont+max]
#                # Rest of chunks
#                while chunk:
#                    query = query_base + ", ".join(chunk)
#                    print "Inserting {0} records".format(len(chunk))
#                    params = {'q': query, 'api_key': api_key}
#                    r = requests.post(self.cartodb_api, data=params)
#                    print r.status_code
#                    print r.text
#                    cont += max
#                    chunk = values[cont:cont+max]
        else:
            print "Something went wrong: {0}".format(r.text)
        
        
        # ONLY FOR TESTING: Remove the table
        #query = "drop table {0}".format(table_name)
        #params = {'q': query, 'api_key': api_key}
        #r = requests.get(self.cartodb_api, params=params)
        #if r.status_code == 200:
        #    print 'Table {0} was deleted'.format(table_name)
        
        return
    
    
    def add_record_to_cartodb(self, record, table_name):
        """Prepare and upload the record to the new cartodb table."""
        
        # Locat mandatory fields

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
        values = "('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}')".format(datasetId, scientificName, decimalLatitude, decimalLongitude, eventDate, recordedBy, json.dumps(extraFields))
        
        return values
        
        ## Old version, record by record, causes timeout
        #query = "insert into {0} (datasetId, scientificName, decimalLatitude, decimalLongitude, eventDate, recordedBy, extraFields) values ({1})".format(table_name, values)
        #
        ## and launch it
        #params = {'q': query, 'api_key': api_key}
        #r = requests.get(self.cartodb_api, params=params)
        #
        #return r
