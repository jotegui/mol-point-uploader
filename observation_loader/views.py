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
@app.route('/upload', methods=['GET','POST'])
def upload():

    up_file = request.files['file']
    
    # TODO: Validate file name and extension
    # TODO: Validate ',' or '\t' separated and store in session
    
    if "useTemplate" in request.form:
        pass # Template used
    
    file_uuid = uuid.uuid4()
    session['file_uuid'] = file_uuid
    session['file_headers'] = up_file.readline().split(",")
    session['file_content'] = up_file.read()
    
    return render_template("/headers.html")


# Metadata about the fields
@app.route('/metafields', methods=['GET','POST'])
def metafields():
    alignment = {
        "scientificName": request.form['scientificName'],
        "latitude": request.form['latitude'],
        "longitude": request.form['longitude'],
        "observationDate": request.form['observationDate'],
        "collector": request.form['collector']
    }
    
    # TODO: Validate content of required headers (above)
    # TODO: Prepare new page for metadata about other fields
    # TODO: Then, redirect to metadata about the project
    
    return render_template("metafields.html")
