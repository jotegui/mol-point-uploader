__author__ = '@jotegui'

import csv
import datetime
from dateutil import parser

from loader_app import app
from flask import session

from google.appengine.ext import ndb

class Parser():
    """Assess the completeness and basic quality of the records."""
    
    def __init__(self):
        """Initialize the class and create storage for headers, errors and warnings."""
        
        # Load content
        blob = ndb.Key(urlsafe=session['raw_key']).get().content
        self.content = csv.reader(blob.split("\n"), delimiter=str(session['field_separator']), quotechar='"')
        
        # Error and warning storage
        self.errors = []
        self.warnings = []
        self.cont = 0
    
    
    def parse_content(self):
        """Evaluate the content of the uploaded file."""
        
        # Process every line
        for record in self.content:
            self.cont += 1
            self.parse_line(record)
        return
    
    
    def parse_line(self, record):
        """Assess each line for all existing quality tests."""
        self.bad_record = False
        
        # Extract values
        vals = {}
        for i in session['mandatory_fields']:
            vals[i] = session['defaults'][i] if session['defaults'][i] != '' else record[session['file_headers'].index(session['headers'][i])]

        # Parse coordinates
        self.parse_coordinates(vals['decimalLatitude'], vals['decimalLongitude'])
        
        # Parse date
        self.parse_eventDate(vals['eventDate'])
        
        # Parse scientificName
        self.parse_scientificName(vals['scientificName'])
        
        # Parse recordedBy
        self.parse_recordedBy(vals['recordedBy'])
        
        # Parse geodeticDatum
        self.parse_geodeticDatum(vals['geodeticDatum'])
        
        # Parse coordinateUncertaintyInMeters
        self.parse_coordinateUncertaintyInMeters(vals['coordinateUncertaintyInMeters'])
        
        # More to be added
        return
    
    
    def parse_coordinates(self, lat, lng):
        """Assess the completeness and quality of the coordinate fields."""
        
        # Completeness
        if lat == "":
#            self.bad_record = True
#            self.errors.append("Latitude missing in record #{0}".format(self.cont))
            return
        if lng == "":
#            self.bad_record = True
#            self.errors.append("Longitude missing in record #{0}".format(self.cont))
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
    
    
    def parse_eventDate(self, date):
        """Assess the completeness and quality of the eventDate field."""
        
        # Completeness
        if date == "":
#            self.bad_record = True
#            self.errors.append("Date missing in record #{0}".format(self.cont))
            return
        
        # Set minimum date to detect Nones
        nulldate = datetime.datetime(datetime.MINYEAR, 1, 1)
        
        # Parse date and if nulldate is returned, return empty
        dt = parser.parse(date, default=nulldate).date()
        if dt == nulldate:
            self.bad_record = True
            self.errors.append("Date could not be recognized in record #{0}".format(self.cont))
            return
        return
    
    
    def parse_scientificName(self, sciname):
        """Assess the completeness and quality of the scientificName field."""
        
        # Completeness
        if sciname == "":
#            self.bad_record = True
#            self.errors.append("Scientific Name missing in record #{0}".format(self.cont))
            return
        
        # Quotes in scientificName
        if "'" in sciname or '"' in sciname:
            self.bad_record = True
            self.errors.append("Strange character (' or \") in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
    
    
    def parse_recordedBy(self, recordedBy):
        """Assess the completeness and quality of the recordedBy field."""
        
        # Completeness
        if recordedBy == "":
#            self.bad_record = True
#            self.errors.append("recordedBy missing in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
    
    
    def parse_geodeticDatum(self, geodeticDatum):
        """Assess the completeness and quality of the geodeticDatum field."""
        
        # Completeness
        if geodeticDatum == "":
#            self.bad_record = True
#            self.errors.append("geodeticDatum missing in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
    
    
    def parse_coordinateUncertaintyInMeters(self, coordinateUncertaintyInMeters):
        """Assess the completeness and quality of the coordinateUncertaintyInMeters field."""
        
        # Completeness
        if coordinateUncertaintyInMeters == "":
#            self.bad_record = True
#            self.errors.append("coordinateUncertaintyInMeters missing in record #{0}".format(self.cont))
            return

        # Values are numbers
        try:
            coordinateUncertaintyInMeters = float(coordinateUncertaintyInMeters)
        except ValueError:
            self.bad_record = True
            self.errors.append("coordinateUncertaintyInMeters is not a number in record #{0}".format(self.cont))
            return
            
        # More to be added
        return
