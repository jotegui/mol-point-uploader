__author__ = '@jotegui'

from datetime import datetime
from flask import render_template, session
from dwc_terms import dwc_terms

def render_eml(request):
    """Render eml.xml template based on data from the request form."""

    file_uuid = session['file_uuid']
    pubDate = format(datetime.today(), "%Y-%m-%d")
    
    # Grab values from request

    # Mandatory fields
    title = request.form['title']
    abstract = request.form['abstract']
    creator_givenName = request.form['resource_creator_first_name']
    creator_surName = request.form['resource_creator_last_name']
    creator_electronicMailAddress = request.form['resource_creator_email']
    metadata_givenName = request.form['metadata_creator_first_name']
    metadata_surName = request.form['metadata_creator_last_name']
    metadata_electronicMailAddress = request.form['metadata_creator_email']
    
    # Optional fields
    lang = request.form['lang'] if 'lang' in request.form.keys() and request.form['lang'] != "" else 'eng'
    intellectualRights = request.form['license'] if 'license' in request.form.keys() else None
    additionalInfo = request.form['additional_information'] if 'additional_information' in request.form.keys() else None
    keywords = [x for x in request.form['keywords'].split(";".rstrip().lstrip())] if len(request.form['keywords']) > 0 else None
    taxonomicCoverage = request.form['taxonomic_scope'] if 'taxonomic_scope' in request.form.keys() else None
    geographicCoverage = request.form['geographic_scope'] if 'geographic_scope' in request.form.keys() else None
    temporalCoverage = request.form['temporal_scope'] if 'temporal_scope' in request.form.keys() else None
    
    # Render template
    eml = render_template("eml.xml",
        file_uuid = file_uuid,
        title = title,
        creator_givenName = creator_givenName,
        creator_surName = creator_surName,
        creator_electronicMailAddress = creator_electronicMailAddress,
        metadata_givenName = metadata_givenName,
        metadata_surName = metadata_surName,
        metadata_electronicMailAddress = metadata_electronicMailAddress,
        pubDate = pubDate,
        lang = lang,
        abstract = abstract,
        intellectualRights = intellectualRights,
        additionalInfo = additionalInfo,
        keywords = keywords,
        taxonomicCoverage = taxonomicCoverage,
        geographicCoverage = geographicCoverage,
        temporalCoverage = temporalCoverage
    ).encode('utf-8')
    
    return eml


def render_meta():
    """Render meta.xml template based on data from the session."""
    
    session.pop('dwc_headers', None)
    session['dwc_headers'] = []
    
    # Initialize field container with 'id' and 'datasetId' as first two elements
    fields = ['id', 'datasetId', 'basisOfRecord']
    defaults = {}
    
    # Make a flat version of the DWC terms
    dwc_terms_flat = {}
    for cl in dwc_terms:
        for t in dwc_terms[cl]:
            dwc_terms_flat[t] = dwc_terms[cl][t]['url']
    
    # Grab values from the session variables
    cont = 0

    for field in session['file_headers']:

        if field in session['headers'].values():
            dwc_term = [x for x in session['headers'] if session['headers'][x] == field][0]
            session['dwc_headers'].append(cont)
            fields.append(dwc_terms_flat[dwc_term])

        elif field in session['extra_fields']:
            if session['extra_fields'][field]['term'] != "":
                session['dwc_headers'].append(cont)
                fields.append(session['extra_fields'][field]['term'])
        cont += 1
    
    # Grab default values
    for field in session['defaults']:
        if session['defaults'][field] != "":
            defaults[dwc_terms_flat[field]] = session['defaults'][field]
    
    # Render template
    meta = render_template("meta.xml", fields=fields, defaults=defaults).encode('utf-8')

    return meta
