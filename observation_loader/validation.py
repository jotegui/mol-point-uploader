from observation_loader import app
from flask import session
import os
import csv

class Parser():
    
    
    def __init__(self):
        """Initialize the class and create storage for errors and warnings."""
        self.errors = []
        self.warnings = []
        self.cont = 0
    
    
    def parse_content(self):
        """Evaluate the content of the uploaded file."""
        # Open file
        with open(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "raw.csv"), 'rb') as csvfile:
            # Create CSV reader object
            csvreader = csv.reader(csvfile, delimiter=session['field_separator'], quotechar='"')
            # Process every line
            for row in csvreader:
                self.cont += 1
                self.parse_line(row)
                
        return
    
    
    def parse_line(self, row):
        """Assess each line for all existing quality tests."""
        # Parse coordinates
        self.parse_coordinates(row)
        
        # Parse date
        self.parse_date(row)
        
        # More to be added
        return
    
    
    def parse_coordinates(self, row):
        """Assess the completeness and quality of coordinates."""
        # Locate latitude and longitude
        lat_field = [x for x in session['alignment'] if session['alignment'][x] == 'decimalLatitude'][0]
        lng_field = [x for x in session['alignment'] if session['alignment'][x] == 'decimalLongitude'][0]
        lat_idx = session['file_headers'].index(lat_field)
        lng_idx = session['file_headers'].index(lng_field)
        lat = row[lat_idx]
        lng = row[lng_idx]
        
        # Completeness
        if lat == "":
            self.errors.append("Latitude missing in record #{0}".format(self.cont))
            return
        if lng == "":
            self.errors.append("Longitude missing in record #{0}".format(self.cont))
            return
        
        # Values are float numbers
        try:
            lat = float(lat)
        except ValueError:
            self.errors.append("Latitude is not a number in record #{0}".format(self.cont))
            return
        try:
            lng = float(lng)
        except ValueError:
            self.errors.append("Longitude is not a number in record #{0}".format(self.cont))
            return
        
        # Both coordinates are 0
        if lat == 0 and lng == 0:
            self.warnings.append("Both coordinates are 0 in record #{0}".format(self.cont))
        
        # Coordinates out of bounds
        if abs(lat)>90:
            if abs(lat)<=180 and abs(lng)<=90:
                self.errors.append("Coordinates might be swapped in record #{0}".format(self.cont))
                return
            else:
                self.errors.append("Latitude out of bounds in record #{0}".format(self.cont))
                return
        if abs(lng)>180:
            self.errors.append("Longitude out of bounds in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
    
    
    def parse_date(self, row):
        """Assess the completeness and quality of dates."""
        
        # Locate date
        date_field = [x for x in session['alignment'] if session['alignment'][x] == 'eventDate'][0]
        date_idx = session['file_headers'].index(date_field)
        date = row[date_idx]
        
        # More to be added
        return
