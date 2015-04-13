__author__ = '@jotegui'

import uuid
import os
import json
import requests

from flask import render_template, redirect, url_for, request, flash, session, g, jsonify

from loader_app import app
from Parser import Parser
from Uploader import Uploader
from dwca_templates import render_eml, render_meta
from dwc_terms import dwc_terms

from helper import mol_user_auth
from cartodb_apikey import api_key

import functions_viz as f
from functions_gcs import GoogleCloudStorage

project_id = 206753940765
bucket_name = "point_uploads"

# Main page
@app.route('/')
@mol_user_auth('MOL_USER')
def main():
    """Return main page."""

    # If coming from parsing content, show errors
    if 'errors' in session.keys():
        errors = session['errors']
    
    # Else, clear session except for any messages and start fresh
    else:
        messages = session.get('_flashes', None)
        session.clear()
        if messages is not None:
            session['_flashes'] = messages
        errors = []

    # Mandatory headers and header types
    session.pop('mandatory_fields_types', None)
    session.pop('mandatory_fields', None)
    
    session['mandatory_fields_types'] = {
        'scientificName': 'text',
        'decimalLatitude': 'number',
        'decimalLongitude': 'number',
        'eventDate': 'text',
        'recordedBy': 'text',
#        'geodeticDatum': 'text',
        'coordinateUncertaintyInMeters': 'number'
    }
    session['mandatory_fields'] = session['mandatory_fields_types'].keys()

    # Tracking variable
    session['from'] = 'main'
    
    return render_template("main.html", errors=errors)


# Help page
@app.route('/help')
@mol_user_auth('MOL_USER')
def help():
    """Return help page."""
    
    return render_template("help.html")


# Spreadsheet template
@app.route('/spreadsheet_template')
@mol_user_auth('MOL_USER')
def download_spreadsheet():
    """Serve xls template to user."""
    
    return redirect(url_for('static', filename='spreadsheet_template.xls'))


# Shortcut to check user data
@app.route('/hello')
@mol_user_auth('MOL_USER')
def hello_user():
    user = g.get('user', None)
    if user:
        return jsonify(username=user['username'],
                       email=user['email'],
                       firstname=user['firstname'],
                       lastname=user['lastname'],
                       id=user['id'])

    return 'Hello Guest'


# Testing site
@app.route('/test')
@mol_user_auth('MOL_USER')
def test():
    
    resp = ""
    
    gcs = GoogleCloudStorage(project_id, bucket_name)
    
    gcs.create_file("1.txt")
    gcs.create_file("2.txt", "Content of the file")
    gcs.create_file("3.txt")
    gcs.create_file("4.txt")
    
    ls = gcs.list_bucket()
    if len(ls) == 4:
        resp += "File creation and listing works properly.<br>"
    
    o = gcs.open_file("2.txt")
    text = o.read()
    o.close()
    if text == "Content of the file":
        resp += "File reading works properly.<br>"
    
    gcs.delete_file("1.txt")
    ls = gcs.list_bucket()
    if len(ls) == 3:
        resp += "Individual deletion works properly.<br>"
    
    gcs.empty_bucket()
    ls = gcs.list_bucket()
    if len(ls) == 0:
        resp += "Bucket emptying works properly."
    
    return resp


# Common operations and template selector
@app.route('/headers_selector', methods = ['GET', 'POST'])
@mol_user_auth('MOL_USER')
def headers_selector():
    """Basic file-level assessment and proper redirection."""
    
    # Generate and store new UUID for file
    file_uuid = str(uuid.uuid4())
    session.pop('file_uuid', None)
    session['file_uuid'] = file_uuid

    # Get file
    up_file = request.files['file']
    if not up_file:
        flash("Please, provide a file to upload")
        return redirect(url_for("main"))
    
    # Parse and upload file to NDB, key in session['raw_key']
    uploader = Uploader()
    uploader.parse_file(up_file)
    if uploader.any_error is True:
        return redirect(url_for('main'))
    
    # Redirect to proper handler
    session['from'] = 'headers_selector'
    if "useTemplate" in request.form:
        return redirect(url_for('with_template'))
    else:
        return redirect(url_for('without_template'))


# With template
@app.route('/with_template')
@mol_user_auth('MOL_USER')
def with_template():
    """Automatically assign headers and defaults."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    session['from'] = 'with_template'
    return redirect(url_for('store_headers'))
    

# Without template
@app.route('/without_template')
@mol_user_auth('MOL_USER')
def without_template():
    """Return header alignment page."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    session['from'] = 'without_template'
    return render_template('headers.html')
    

@app.route('/store_headers', methods=['GET', 'POST'])
@mol_user_auth('MOL_USER')
def store_headers():
    """Store headers in session variables."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    session.pop('headers', None)
    
    # If GET request, template is used
    if request.method == 'GET':
        
        # Store template headers
        session.pop('headers', None)
        session['headers'] = {}
        for i in session['mandatory_fields']:
            session['headers'][i] = unicode(i)
        
        # Check if template is actually used
        for i in session['file_headers']:
            if i not in session['headers']:
                flash("We could not recognize the template. Redirected to header alignment")
                return redirect(url_for('without_template'))
        
        # Store empty default values
        session.pop('defaults', None)
        session['defaults'] = {}
        for i in session['mandatory_fields']:
            session['defaults'][i] = ""
    
    # If POST request, template is not used
    elif request.method == 'POST':
        
        # Store header alignment
        session.pop('headers', None)
        session['headers'] = {}
        for i in session['mandatory_fields']:
            session['headers'][i] = unicode(request.form[i]) if request.form[i] != "? undefined:undefined ?" else ""
        
        # Store default values
        session.pop('defaults', None)
        session['defaults'] = {}
        for i in session['mandatory_fields']:
            session['defaults'][i] = unicode(request.form[i+'Default'])
    
    session['from'] = 'with_template'
    return redirect(url_for('parse'))


@app.route('/parse')
@mol_user_auth('MOL_USER')
def parse():
    """Check the consistency of the uploaded file."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    parser = Parser()
    uploader = Uploader()
    f = uploader.open_file(session['file_uuid'])
    parser.parse_content(f)
    
    if len(parser.errors) == 0:
        target = 'metafields'
    else:
        session.pop('errors', None)
        session['errors'] = parser.errors
        flash('ERROR: We found some problems when parsing your file. <a href="#" data-toggle="modal" data-target="#parsingModal">Click here</a> to get a detailed review.')
        target = 'main'
    return redirect(url_for(target))


@app.route('/metafields', methods = ['GET', 'POST'])
@mol_user_auth('MOL_USER')
def metafields():
    """Assess presence of extra fields and redirect properly."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    # Prepare extra fields for metadata
    extra_fields = [x for x in session['file_headers'] if x not in session['headers'].values() and x not in session['headers'].keys()]
    session.pop('extra_fields', None)
    session['extra_fields'] = extra_fields
    
    # Decide where to go
    if len(extra_fields) > 0:
        session['from'] = 'metafields'
        return render_template('metafields.html', dwc_terms = dwc_terms)
    else:
        return redirect(url_for('metadata'))


@app.route('/metadata', methods = ['GET', 'POST'])
@mol_user_auth('MOL_USER')
def metadata():
    """Store extra fields, if any, and prepare and upload meta.xml."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    # Parse metafields if coming from there
    if session['from'] == 'metafields':
        session['extra_fields'] = {}

        for i in request.form.keys():
            if i != 'submitBtn' and not i.endswith("_dwc"):
                term_dict = {"description": request.form[i], "term": request.form["%s_dwc" % i]}
                session['extra_fields'][i] = term_dict
    
    # Create meta.xml
    meta = render_meta()
    
    # Upload to NDB datastore
    uploader = Uploader()
    uploader.upload_meta(meta)
    
    # Render metadata template
    session['from'] = 'metadata'
    return render_template('metadata.html')


@app.route('/upload', methods = ['POST'])
@mol_user_auth('MOL_USER')
def upload():
    """Render and upload eml.xml, and create entry in registry table."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    # Create eml.xml
    eml = render_eml(request)
    
    # Upload to NDB datastore
    uploader = Uploader()
    uploader.upload_eml(eml)
    
    # Create CartoDB registry record
    success = uploader.cartodb_meta(request.form)
    if success == False:
        return render_template('metadata.html')
    
    # Store datum
    session.pop('geodeticDatum', None)
    session['geodeticDatum'] = request.form['datum'] if 'datum' in request.form and request.form['datum'] != "" else "WGS84"
    
    # Create occurrence.txt
#    uploader.build_occurrence()
    # TODO: Implement build_dwca and move to Cloud Storage with googleapis    

    session['from'] = 'upload'
    return render_template('upload_cartodb.html')


@app.route('/upload_cartodb')
@mol_user_auth('MOL_USER')
def upload_cartodb():
    """Parse records and upload to point table."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    uploader = Uploader()
    
    # Prepare the file for CartoDB
    uploader.cartodb_points()
    
    # Delete everything NDB datastore
    #uploader.delete_entity('raw_key')
    uploader.delete_entity('meta_key')
    uploader.delete_entity('eml_key')
    #uploader.delete_entity('occurrence_key')
    
    # Go back to main page
    return redirect(url_for('records', datasetid=session['file_uuid']))


@app.route('/datasets')
@mol_user_auth('MOL_USER')
def datasets():
    """Dashboard"""
    
    current_user = g.get('user', None)
    if current_user:
        entries = f.get_datasets_data(current_user)
    else:
        entries = None
    
    return render_template('user/datasets.html', entries=entries)


@app.route('/records/<datasetid>')
@mol_user_auth('MOL_USER')
def records(datasetid):
    """User submitted species observations via the point uploader, table view"""
    
    current_user = g.get('user', None)
    if current_user:
        entries, title, centroid, species = f.get_points_data(current_user, datasetid)
    else:
        entries = None
        title = None
        centroid = None
        species = None

    return render_template('user/records.html', entries=entries, title=title, datasetid=datasetid, centroid=centroid, species=species)


@app.route('/delete/<datasetid>')
@mol_user_auth('MOL_USER')
def delete(datasetid):
    """Delete user submitted dataset"""

    current_user = g.get('user', None)
    if current_user:
        success = f.delete_dataset(current_user, datasetid)
        if success is True:
            flash("Dataset successfully deleted")
        else:
            flash("ERROR: Dataset could not be deleted")
    return redirect(url_for("datasets"))
