import uuid
import os
import json

from flask import flash, render_template, g
from observation_loader import app
from observation_loader.validator import validate
from observation_loader.util import allowed_file

def upload_archive(request):

    # Redirect to home page if no file is being uploaded
    if request.method == 'GET':
        return 'main', None
        
    file = request.files['file']
    if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)
        
        # Generate UUID
        file_uuid = uuid.uuid4()
        foldername = os.path.join(app.config['UPLOAD_FOLDER'], str(file_uuid))
        filename = '.'.join([str(file_uuid), 'csv'])
        
        # Parse content
        content = file.read()
        errors, warnings = validate(content, request.form)
        g.content = content

        # Show errors
        if len(warnings)>0:
            for i in warnings:
                flash(i)
        if len(errors)>0:
            for i in errors:
                flash(i)
            return 'main', None
        else:
            # Save file as [UUID].csv
            os.mkdir(foldername)
            file_path = os.path.join(foldername, filename)
            file.save(file_path)
            flash("File was uploaded successfully. A new UUID has been generated for this file:\n{0}".format(str(file_uuid)))
            answer = {"conten":content, "uuid": str(file_uuid)}
            return 'headers', answer
    
    else:
        flash("ERROR: Wrong file format. You must provide a \".csv\" file")
        return 'main', None


def upload_meta(request):
    formdata = request.form
    meta = {
        "public": "{0}".format(True if 'public' in formdata else False),
        "title": "{0}".format(formdata['title']),
        "resource_creator": "{0}".format(formdata['resource_creator']),
        "metadata_creator": "{0}".format(formdata['metadata_creator']),
        "geographic_scope": "{0}".format(formdata['geographic_scope']),
        "temporal_scope": "{0}".format(formdata['temporal_scope']),
        "keywords": "{0}".format(formdata['keywords']),
        "abstract": "{0}".format(formdata['abstract']),
        "license": "{0}".format(formdata['license']),
        "additional_information": "{0}".format(formdata['additional_information'])
    }
    
    file_uuid = request.form['file_uuid']
    foldername = os.path.join(app.config['UPLOAD_FOLDER'], file_uuid)
    filename = "metadata.json"
    file_path = os.path.join(foldername, filename)

    with open(file_path, 'w') as w:
        w.write(json.dumps(meta))
    
    flash("Congratulations. Your file and metadata have been uploaded successfully. You should be able to access them in the list below.")

    return 'main'
