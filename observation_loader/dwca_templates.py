from datetime import datetime
from flask import render_template

def render_eml(request):
    """Render eml.xml template based on data from the request form."""
    
    # Grab values from request
    title = request.form['title']
    creator_givenName = request.form['resource_creator_first_name']
    creator_surName = request.form['resource_creator_last_name']
    creator_electronicMailAddress = request.form['resource_creator_email']
    metadata_givenName = request.form['metadata_creator_first_name']
    metadata_surName = request.form['metadata_creator_last_name']
    metadata_electronicMailAddress = request.form['metadata_creator_email']
    pubDate = format(datetime.today(), "%Y-%m-%d")
    abstract = request.form['abstract']
    intellectualRights = request.form['license'] if 'license' in request.form.keys() else None
    additionalInfo = request.form['additional_information'] if 'additional_information' in request.form.keys() else None
    keywords = [x for x in request.form['keywords'].split(";".rstrip().lstrip())] if len(request.form['keywords']) > 0 else None
    taxonomicCoverage = request.form['taxonomic_scope'] if 'taxonomic_scope' in request.form.keys() else None
    geographicCoverage = request.form['geographic_scope'] if 'geographic_scope' in request.form.keys() else None
    temporalCoverage = request.form['temporal_scope'] if 'temporal_scope' in request.form.keys() else None
    
    # Render template
    eml = render_template("eml.xml",
        title = title,
        creator_givenName = creator_givenName,
        creator_surName = creator_surName,
        creator_electronicMailAddress = creator_electronicMailAddress,
        metadata_givenName = metadata_givenName,
        metadata_surName = metadata_surName,
        metadata_electronicMailAddress = metadata_electronicMailAddress,
        pubDate = pubDate,
        abstract = abstract,
        intellectualRights = intellectualRights,
        additionalInfo = additionalInfo,
        keywords = keywords,
        taxonomicCoverage = taxonomicCoverage,
        geographicCoverage = geographicCoverage,
        temporalCoverage = temporalCoverage
    )
    
    return eml
