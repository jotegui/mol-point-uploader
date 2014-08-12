import csv
import StringIO
from observation_loader.util import safe_unicode, safe_str

errors = []
warnings = []
template_schema = ["Scientific name", "Latitude", "Longitude", "Observation date", "Collector", "Geodetic datum", "Sampling method", "Verbatim locality", "Coordinate uncertainty"]

def validate(content, form):
    
    # Open the content as a csv "file-like" object, for the csv module
    data = StringIO.StringIO(content)
    
    reader = csv.reader(data, delimiter=',', quotechar='"')
    
    cont = 1
    all_errors = []
    all_warnings = []
    
    for row in reader:
        
        # Skip headers
        if row[0] in template_schema:
            continue

        global errors
        errors = []
        global warnings
        warnings = []
        
        # Check mandatory fields
        check_mandatory(row)
        
        # Check coordinates
        check_coordinates(row[1], row[2])
        
        # Check date format
        check_date_format(row[3])
        
        for error in errors:
            all_errors.append(safe_str(safe_unicode("ERROR: Row #{0}: {1}".format(cont, error))))
        for warning in warnings:
            all_warnings.append(safe_str(safe_unicode("WARNING: Row #{0}: {1}".format(cont, warning))))

        cont += 1
    
    # Close the object to free memory
    data.close()
    
    return all_errors, all_warnings

def throw_validation(valid, errors, warnings):
    return {"valid": valid, "errors": errors, "warnings": warnings}

def check_mandatory(row):
    for x in [0, 1, 2, 3, 4]:
        if len(row[x]) == 0:
            global errors
            errors.append("{0} value missing".format(template_schema[x]))
    return
        

def check_coordinates(lat, lon):
    
    valid = None
    global errors
    global warnings
    
    if len(lat)==0 or len(lon)==0:
        return
    
    # Check if latitude and longitude are numbers
    try:
        float(lat)
    except ValueError:
        valid = False
        errors.append("Non-numeric value in latitude: {0}".format(lat))
    finally:
        try:
            float(lon)
        except ValueError:
            valid = False
            errors.append("Non-numeric value in longitude: {0}".format(lon))
        finally:
            if valid is False:
                return
    
    lat = float(lat)
    lon = float(lon)
    
    # Check if both coordinates are 0
    if lat==0 and lon==0:
        warnings.append("Both coordinates are 0")
    
    # Check if coordinates are out of bounds
    if abs(lat)>90:
        valid = False
        errors.append("Latitude value out of bounds: {0}".format(lat))
    if abs(lon)>180:
        valid = False
        errors.append("Longitude value out of bounds:{0}".format(lon))
    if valid is False:
        return
    
    return

def check_date_format(occdate):
    global errors
    global warnings
    
    try:
        feats = occdate.split('-')
        feats[2]
    except IndexError:
        errors.append("Malformed observation date: {0}".format(occdate))
        return
    
    if len(feats[0]) != 4:
        errors.append("Malformed year in observation date: {0}".format(occdate))
    if len(feats[1]) != 2:
        errors.append("Malformed month in observation date: {0}".format(occdate))
    if len(feats[2]) != 2:
        errors.append("Malformed day in observation date: {0}".format(occdate))
