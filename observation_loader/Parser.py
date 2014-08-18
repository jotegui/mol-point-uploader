from observation_loader import app
from flask import session
import os
import csv
import uuid

class Parser():
    """Assess the completeness and basic quality of the records, and create a Darwin Core Archive."""
    
    def __init__(self, dataset_uuid):
        """Initialize the class and create storage for errors and warnings."""
        self.dataset_uuid = dataset_uuid
        self.errors = []
        self.warnings = []
        self.cont = 0
        
    
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
    
    
    def parse_content(self):
        """Evaluate the content of the uploaded file."""
        with open(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "raw.csv"), 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=session['field_separator'], quotechar='"')
            # Process every line
            for record in csvreader:
                self.cont += 1
                self.parse_line(record)
            return
    
    
    def parse_line(self, record):
        """Assess each line for all existing quality tests."""
        self.bad_record = False
        
        # Parse coordinates
        self.parse_coordinates(record)
        
        # Parse date
        self.parse_date(record)
        
        # More to be added
        return
    
    
    def parse_coordinates(self, record):
        """Assess the completeness and quality of coordinates."""
        # Locate latitude and longitude
        lat_field = [x for x in session['alignment'] if session['alignment'][x] == 'decimalLatitude'][0]
        lng_field = [x for x in session['alignment'] if session['alignment'][x] == 'decimalLongitude'][0]
        lat_idx = session['file_headers'].index(lat_field)
        lng_idx = session['file_headers'].index(lng_field)
        lat = record[lat_idx]
        lng = record[lng_idx]
        
        # Completeness
        if lat == "":
            self.bad_record = True
            self.errors.append("Latitude missing in record #{0}".format(self.cont))
            return
        if lng == "":
            self.bad_record = True
            self.errors.append("Longitude missing in record #{0}".format(self.cont))
            return
        
        # Values are float numbers
        try:
            lat = float(lat)
        except ValueError:
            self.bad_record = True
            self.errors.append("Latitude is not a number in record #{0}".format(self.cont))
            return
        try:
            lng = float(lng)
        except ValueError:
            self.bad_record = True
            self.errors.append("Longitude is not a number in record #{0}".format(self.cont))
            return
        
        # Both coordinates are 0
        if lat == 0 and lng == 0:
            self.warnings.append("Both coordinates are 0 in record #{0}".format(self.cont))
        
        # Coordinates out of bounds
        if abs(lat)>90:
            if abs(lat)<=180 and abs(lng)<=90:
                self.bad_record = True
                self.errors.append("Coordinates might be swapped in record #{0}".format(self.cont))
                return
            else:
                self.bad_record = True
                self.errors.append("Latitude out of bounds in record #{0}".format(self.cont))
                return
        if abs(lng)>180:
            self.bad_record = True
            self.errors.append("Longitude out of bounds in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
    
    
    def parse_date(self, record):
        """Assess the completeness and quality of dates."""
        
        # Locate date
        date_field = [x for x in session['alignment'] if session['alignment'][x] == 'eventDate'][0]
        date_idx = session['file_headers'].index(date_field)
        date = record[date_idx]
        
        # More to be added
        return
