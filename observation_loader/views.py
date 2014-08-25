from observation_loader import app
from Parser import Parser
from Uploader import Uploader
from dwca_templates import render_eml, render_meta
from dwc_terms import dwc_terms
import uuid
import os
from zipfile import ZipFile

from flask import render_template, redirect, url_for, request, send_from_directory, flash, session
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt','csv','tsv'])

# Main page
@app.route('/')
def main():
    return render_template("file_upload.html")

# Help page
@app.route('/help')
def help():
    return render_template("help.html")


# Spreadsheet template
@app.route('/spreadsheet_template')
def download_spreadsheet():
    return redirect(url_for('static', filename='spreadsheet_template.xls'))


# File upload
@app.route('/headers', methods=['GET','POST'])
def headers():

    # Get file
    up_file = request.files['file']
    if not up_file:
        flash("Please, provide a file to upload")
        return redirect(url_for("main"))
    
    # Check for allowed file extension
    allowed_file = '.' in up_file.filename and up_file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    if allowed_file is False:
        flash("ERROR: Unsupported file type. File should be .txt, .csv or .tsv")
        return redirect(url_for('main'))
    
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
        return redirect(url_for('main'))
    
    # Generate new UUID for file
    file_uuid = str(uuid.uuid4())
    session.pop('file_uuid', None)
    session['file_uuid'] = file_uuid
    
    # create the folder
    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], file_uuid))
    # and save the file
    up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_uuid, "raw.csv"))
    
    # Store headers
    session.pop('file_headers', None)
    session['file_headers'] = headerline.split(session['field_separator'])
    
    # Remove some extra values from session
    session.pop('alignment', None)
    session.pop('extra_fields', None)
    
    # If they are using our template
    if "useTemplate" in request.form:
        
        # We already know the names of the required fields
        session['alignment'] = {
            "scientificName": 'scientificName',
            "decimalLatitude": 'decimalLatitude',
            "decimalLongitude": 'decimalLongitude',
            "eventDate": 'eventDate',
            "recordedBy": 'recordedBy'
        }
        
        full_schema = session['alignment']
        full_schema["geodeticDatum"] = 'geodeticDatum'
        full_schema["samplingProtocol"] = 'samplingProtocol'
        full_schema["verbatimLocality"] = 'verbatimLocality'
        full_schema["coordinateUncertaintyInMeters"] = 'coordinateUncertaintyInMeters'
        
        # Check if template was actually used
        missing = [x for x in session['alignment'] if x not in session['file_headers']]
        if len(missing) > 0:
            flash("ERROR: The following fields are missing from the template: {0}".format(", ".join(missing)))
            return redirect(url_for("main"))
        
        # Parse the content
        parser = Parser()
        parser.parse_content()
        if len(parser.errors) > 0:
            for i in parser.errors:
                flash("ERROR: {0}".format(i))
            flash("Please, fix these issues or remove the wrong records and try again.")
            return redirect(url_for('main'))
        
        # Maybe, check for some extra fields in case they extended the template
        extra_fields = [x for x in session['file_headers'] if x not in full_schema.values()]
        
        # If so, point to the metafields page
        if len(extra_fields) > 0:
            return render_template("metafields.html", extra_fields=extra_fields, dwc_terms=dwc_terms)
        # Else, to the metadata page
        else:
            return render_template("metadata.html")
    
    # If they are not using our template,
    else:
        
        # And go to header processing
        return render_template("/headers.html")


# Metadata about the fields
@app.route('/metafields', methods=['GET','POST'])
def metafields():
    
    # Process alignment
    session['alignment'] = {
        request.form['scientificName']: "scientificName",
        request.form['decimalLatitude']: "decimalLatitude",
        request.form['decimalLongitude']: "decimalLongitude",
        request.form['eventDate']: "eventDate",
        request.form['recordedBy']: "recordedBy"
    }
    
    print session['alignment'].values()
    
    # Parse the content
    parser = Parser()
    parser.parse_content()
    if len(parser.errors) > 0:
        for i in parser.errors:
            flash("ERROR: {0}".format(i))
        flash("Please, fix these issues or remove the wrong records and try again.")
        return redirect(url_for('main'))

    # Prepare extra fields for metadata
    extra_fields = [x for x in session['file_headers'] if x not in session['alignment'].keys()]
    
    if len(extra_fields) > 0:
        return render_template("metafields.html", extra_fields=extra_fields, dwc_terms=dwc_terms)
    else:
        return render_template("metadata.html")


# General metadata
@app.route('/metadata', methods=['GET', 'POST'])
def metadata():
    
    session['extra_fields'] = {}
    for i in request.form.keys():
        if i != 'submitBtn' and not i.endswith("_dwc"):
            term_dict = {"description": request.form[i], "term": request.form["{0}_dwc".format(i)]}
            session['extra_fields'][i] = term_dict
    
    meta = render_meta()
    meta_path = os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "meta.xml")
    with open(meta_path, 'w') as w:
        w.write(meta)
    
    return render_template("metadata.html")


# Build DarwinCore Archive
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    # Create eml.xml
    eml = render_eml(request)
    eml_path = os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "eml.xml")
    with open(eml_path, 'w') as w:
        w.write(eml)
    
    # Create occurrence.txt
    uploader = Uploader()
    uploader.build_occurrence()
    
    # Wrap the DwC-A in a zip file
    with ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid']+'.zip'),'w') as dwca:
        dwca.write(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "eml.xml"), "eml.xml")
        dwca.write(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "meta.xml"), "meta.xml")
        dwca.write(os.path.join(app.config['UPLOAD_FOLDER'], session['file_uuid'], "occurrence.txt"), "occurrence.txt")
    
    return render_template('upload_cartodb.html')


@app.route('/upload_cartodb')
def upload_cartodb():
    
    # Prepare the file for CartoDB
    uploader = Uploader()
    uploader.build_cartodb()
    
    return redirect(url_for('main'))
