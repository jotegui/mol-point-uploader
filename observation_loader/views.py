from observation_loader import app
import uuid

from flask import render_template, redirect, url_for, request, send_from_directory, flash, session
from werkzeug.utils import secure_filename


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

    up_file = request.files['file']
    file_uuid = uuid.uuid4()
    
    # TODO: Validate file name and extension
    # TODO: Validate ',' or '\t' separated and store in session
    
    #if "useTemplate" in request.form:
    #    pass # TODO: Skip metafields if template used
    
    session.pop('file_uuid', None)
    session['file_uuid'] = file_uuid
    print file_uuid
    
    session.pop('file_headers', None)
    session['file_headers'] = up_file.readline().rstrip().split(",")
    
    return render_template("/headers.html")


# Metadata about the fields
@app.route('/metafields', methods=['GET','POST'])
def metafields():
    
    # Process alignment
    session.pop('alignment', None)
    session['alignment'] = {
        "scientificName": request.form['scientificName'],
        "latitude": request.form['latitude'],
        "longitude": request.form['longitude'],
        "observationDate": request.form['observationDate'],
        "collector": request.form['collector']
    }
    
    # TODO: Validate content of required headers (above)

    # Prepare extra fields for metadata
    extra_fields = [x for x in session['file_headers'] if x not in session['alignment'].values()]
    
    return render_template("metafields.html", extra_fields = extra_fields)


# General metadata
@app.route('/metadata', methods=['GET', 'POST'])
def metadata():
    session.pop('extra_fields', None)
    session['extra_fields'] = []
    for i in request.form.keys():
        if i != 'submitBtn':
            session['extra_fields'].append({i: request.form[i]})
    print session['alignment']
    print session['extra_fields']
    return render_template("metadata.html")


# Last step
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    # TODO: Parse content, create SQL and execute it
    
    flash('File uploaded successfuly!')
    return redirect(url_for('main'))
