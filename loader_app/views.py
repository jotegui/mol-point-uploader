__author__ = '@jotegui'

import uuid
import os
import json

from flask import render_template, redirect, url_for, request, flash, session

from loader_app import app
from Parser import Parser
from Uploader import Uploader
from dwca_templates import render_eml, render_meta
from dwc_terms import dwc_terms
import functions as f


# Main page
@app.route('/')
def main():
    """Return main page."""
    
    # If coming from parsing content, show errors
    print session
    if 'errors' in session.keys():
        errors = session['errors']
    # Otherwise, clear session and start fresh
    else:
        session.clear()
        errors = []
    
    # Mandatory headers and header types
    session.pop('mandatory_fields_types', None)
    session.pop('mandatory_fields', None)
    
    session['mandatory_fields_types'] = {
        'scientificName': 'text',
        'decimalLatitude': 'number',
        'decimalLongitude': 'number',
        'eventDate': 'date',
        'recordedBy': 'text',
        'geodeticDatum': 'text',
        'coordinateUncertaintyInMeters': 'number'
    }
    session['mandatory_fields'] = session['mandatory_fields_types'].keys()
    
    # Tracking variable
    session['from'] = 'main'
    
    return render_template("main.html", errors=errors)


# Help page
@app.route('/help')
def help():
    """Return help page."""
    
    return render_template("help.html")


# Spreadsheet template
@app.route('/spreadsheet_template')
def download_spreadsheet():
    """Serve xls template to user."""
    
    return redirect(url_for('static', filename='spreadsheet_template.xls'))


# Common operations and template selector
@app.route('/headers_selector', methods = ['GET', 'POST'])
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
def with_template():
    """Automatically assign headers and defaults."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    session['from'] = 'with_template'
    return redirect(url_for('store_headers'))
    

# Without template
@app.route('/without_template')
def without_template():
    """Return header alignment page."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    session['from'] = 'without_template'
    return render_template('headers.html')
    

@app.route('/store_headers', methods=['GET', 'POST'])
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
            session['headers'][i] = i
        
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
            session['headers'][i] = request.form[i] if request.form[i] != "? undefined:undefined ?" else ""
        
        # Store default values
        session.pop('defaults', None)
        session['defaults'] = {}
        for i in session['mandatory_fields']:
            session['defaults'][i] = request.form[i+'Default']
    
    session['from'] = 'with_template'
    return redirect(url_for('parse'))


@app.route('/parse')
def parse():
    """Check the consistency of the uploaded file."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    parser = Parser()
    parser.parse_content()
    
    if len(parser.errors) == 0:
        target = 'metafields'
    else:
        session.pop('errors', None)
        session['errors'] = parser.errors
        flash('ERROR: We found some problems when parsing your file. <a href="#" data-toggle="modal" data-target="#parsingModal">Click here</a> to get a detailed review.')
        target = 'main'
    return redirect(url_for(target))


@app.route('/metafields', methods = ['GET', 'POST'])
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
    uploader.cartodb_meta(request.form)
    
    # Create occurrence.txt
#    uploader.build_occurrence()
    # TODO: Implement build_dwca and move to Cloud Storage with googleapis    

    session['from'] = 'upload'
    return render_template('upload_cartodb.html')


@app.route('/upload_cartodb')
def upload_cartodb():
    """Parse records and upload to point table."""
    
    if 'file_uuid' not in session.keys():
        return redirect(url_for('main'))
    
    uploader = Uploader()
    
    # Prepare the file for CartoDB
    uploader.cartodb_points()
    
    # Delete everything NDB datastore
    uploader.delete_entity('raw_key')
    uploader.delete_entity('meta_key')
    uploader.delete_entity('eml_key')
    #uploader.delete_entity('occurrence_key')
    
    # Go back to main page
    return redirect(url_for('main'))
