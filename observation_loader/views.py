from observation_loader import app

from flask import render_template, redirect, url_for, request, send_from_directory, flash
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
    
    if "useTemplate" in request.form:
        pass # Template used
    
    headers = up_file.readline().split(",")
    return render_template("/headers.html", headers=headers)


# Metadata about the fields
@app.route('/metafields', methods=['GET','POST'])
def metafields():
    return render_template("metafields.html")
