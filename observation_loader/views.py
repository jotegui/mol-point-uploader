from observation_loader import app
from observation_loader.uploader import upload_archive, upload_meta

from flask import render_template, redirect, url_for, request, send_from_directory, flash, g
from werkzeug.utils import secure_filename


# Main page
@app.route('/')
def main():
    return render_template("file_upload.html")

# Help page
@app.route('/help')
def help():
    return render_template("help.html")


# Header form
@app.route('/headers')
def headers():
    print g.content
    return render_template("headers.html")

# Metadata form
@app.route('/meta')
def meta():
    return render_template("meta.html")


# Spreadsheet template
@app.route('/spreadsheet_template')
def download_spreadsheet():
    return redirect(url_for('static', filename='spreadsheet_template.xls'))


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    
    if request.form['origin'] == 'file_upload':
        where_to, content = upload_archive(request)
    
    elif request.form['origin'] == 'metadata':
        content = None
        where_to = upload_meta(request)
    
    if content is not None:
        return redirect("{0}?uuid={1}".format(url_for(where_to), content['uuid']))
    else:
        return redirect(url_for(where_to))


@app.route('/dataset/<uuid>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], uuid, uuid))

