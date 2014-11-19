__author__ = '@jotegui'

import csv
from datetime import datetime

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
        for i in ['decimalLatitude','decimalLongitude','eventDate','scientificName', 'recordedBy']:
            vals[i] = session['defaults'][i] if session['defaults'][i] != '' else record[session['file_headers'].index(session['headers'][i])]

        # Parse coordinates
        self.parse_coordinates(vals['decimalLatitude'], vals['decimalLongitude'])
        
        # Parse date
        self.parse_eventDate(vals['eventDate'])
        
        # Parse scientificName
        self.parse_scientificName(vals['scientificName'])
        
        # Parse recordedBy
        self.parse_recordedBy(vals['recordedBy'])
        
        # More to be added
        return
    
    
    def parse_coordinates(self, lat, lng):
        """Assess the completeness and quality of coordinates."""
        
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
    
    
    def parse_eventDate(self, date):
        """Assess the completeness and quality of dates."""
        
        # Accepted date field separators: "/", "-", "."
        accepted_separators = ['/', '-', '.']
        
        # Completeness
        if date == "":
            self.bad_record = True
            self.errors.append("Date missing in record #{0}".format(self.cont))
            return
        
        # Accepted date formats
        
        # Year only
        if len(date) == 4:
            # Check if is number
            try:
                int(date)
            except ValueError:
                self.bad_record = True
                self.errors.append("Invalid date format in record #{0}".format(self.cont))
                return
                
            # Check if within reasonable years (1750 - this year)
            if int(date) < 1750 or int(date) > datetime.today().year:
                self.bad_record = True
                self.errors.append("Year out of range in record #{0}".format(self.cont))
                return
                
        # Year-month, without separator
        elif len(date) == 6:
            # Check if correct format
            try:
                int(date[:4])
                int(date[4:])
            except ValueError:
                self.bad_record = True
                self.errors.append("Invalid date format in record #{0}".format(self.cont))
                return
                
            # Check if year within reasonable years (1750 - this year)
            if int(date[:4]) < 1750 or int(date[:4]) > datetime.today().year:
                self.bad_record = True
                self.errors.append("Year out of range in record #{0}".format(self.cont))
                return
                
            # Check if month within accepted range
            if int(date[4:]) < 1 or int(date[4:]) > 12:
                self.bad_record = True
                self.errors.append("Month out of range in record #{0}".format(self.cont))
                return
                
        # Year-month with separator.
        elif len(date) == 7:
            # Check if correct format
            try:
                int(date[:4])
                int(date[5:])
            except ValueError:
                self.bad_record = True
                self.errors.append("Invalid date format in record #{0}".format(self.cont))
                return
                
            if date[4] not in accepted_separators:
                self.bad_record = True
                self.errors.append("Invalid date field separator in record #{0}".format(self.cont))
                return
                
            # Check if year within reasonable years (1750 - this year)
            if int(date[:4]) < 1750 or int(date[:4]) > datetime.today().year:
                self.bad_record = True
                self.errors.append("Year out of range in record #{0}".format(self.cont))
                return
                
            # Check if month within accepted range
            if int(date[5:]) < 1 or int(date[5:]) > 12:
                self.bad_record = True
                self.errors.append("Month out of range in record #{0}".format(self.cont))
                return
                
        # TODO: Update adding final case (year-month-day with separator and both month and day with single-digit values)
        # Year-month-day, without separator, or year-month-day with separator and both month and day with single-digit values
        elif len(date) == 8:
            # Check if correct format
            try:
                int(date[:4])
                int(date[4:6])
                int(date[6:])
            except ValueError:
                self.bad_record = True
                self.errors.append("Invalid date format in record #{0}".format(self.cont))
            return
            
            # Check if year within reasonable years (1750 - this year)
            if int(date[:4]) < 1750 or int(date[:4]) > datetime.today().year:
                self.bad_record = True
                self.errors.append("Year out of range in record #{0}".format(self.cont))
                return
                
            # Check if month within accepted range
            if int(date[4:6]) < 1 or int(date[4:6]) > 12:
                self.bad_record = True
                self.errors.append("Month out of range in record #{0}".format(self.cont))
                return
                
            # Check if day within accepted range
            if int(date[6:]) < 1 or int(date[6:]) > 31:
                self.bad_record = True
                self.errors.append("Day out of range in record #{0}".format(self.cont))
                return
        
        
        # TODO: complete this
        # Year-month-day, with either month or day with single-digit value
        elif len(date) == 9:
            pass
        
        
        # Year-month-day with separator.
        elif len(date) == 10:
            # Check if correct format
            try:
                int(date[:4])
                int(date[5:7])
                int(date[8:])
            except ValueError:
                self.bad_record = True
                self.errors.append("Invalid date format in record #{0}".format(self.cont))
                return
                
            if date[4] not in accepted_separators or date[7] not in accepted_separators or date[4] != date[7]:
                self.bad_record = True
                self.errors.append("Invalid date field separator in record #{0}".format(self.cont))
                return
                
            # Check if year within reasonable years (1750 - this year)
            if int(date[:4]) < 1750 or int(date[:4]) > datetime.today().year:
                self.bad_record = True
                self.errors.append("Year out of range in record #{0}".format(self.cont))
                return
                
            # Check if month within accepted range
            if int(date[5:7]) < 1 or int(date[5:7]) > 12:
                self.bad_record = True
                self.errors.append("Month out of range in record #{0}".format(self.cont))
                return
                
            # Check if day within accepted range
            if int(date[8:]) < 1 or int(date[8:]) > 31:
                self.bad_record = True
                self.errors.append("Day out of range in record #{0}".format(self.cont))
                return
            
        # More to be added
        else:
            self.bad_record = True
            self.errors.append("Unrecognised date format in record #{0}".format(self.cont))
            return
        
        return
    
    
    def parse_scientificName(self, sciname):
        """Assess the completeness and quality of scientific names."""
        
        # Completeness
        if sciname == "":
            self.bad_record = True
            self.errors.append("Scientific Name missing in record #{0}".format(self.cont))
            return
        
        # Quotes in scientificName
        if "'" in sciname or '"' in sciname:
            self.bad_record = True
            self.errors.append("Strange character (' or \") in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
    
    
    def parse_recordedBy(self, recordedBy):
        """Assess the completeness and quality of scientific names."""
        
        # Completeness
        if recordedBy == "":
            self.bad_record = True
            self.errors.append("recordedBy missing in record #{0}".format(self.cont))
            return
        
        # More to be added
        return
