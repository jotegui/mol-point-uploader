__author__ = '@jotegui'

from cartodb_apikey import api_key
import requests

def get_datasets_data(current_user):
    """Get values for listing available datasets for user."""
    
    email = current_user['email']
    q = "select datasetid, title, created_at, creatoremail, creatorfirst, creatorlast, metadataemail, metadatafirst, metadatalast, public, license, geographicscope, temporalscope, taxonomicscope from point_uploads_registry where email='{0}'".format(email)
    params = {'q': q, 'api_key': api_key}
    r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
    if r.status_code == 200:
        entries = r.json()['rows']
    else:
        entries = None
    
    return entries


def get_points_data(current_user, datasetid):
    """Get values for rendering points in map visualization."""
    
    email = current_user['email']
    
    # Get points
    q = "select * from point_uploads_master where datasetid='{0}'".format(datasetid)
    params = {'q': q, 'api_key': api_key}
    r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
    if r.status_code == 200:
        entries = r.json()['rows']
    else:
        entries = None
    
    # Get layergroupid and title
    q = "select title from point_uploads_registry where datasetid='{0}'".format(datasetid)
    params = {'q': q, 'api_key': api_key}
    r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
    if r.status_code == 200:
        title = r.json()['rows'][0]['title']
    else:
        title = None
        
    # Get centroid
    q = "select ST_X(centroid) as lng, ST_Y(centroid) as lat from (select ST_Centroid(ST_Union(the_geom)) as centroid from (select the_geom from point_uploads_master where datasetid='{0}') as foo) as bar".format(datasetid)
    params = {'q': q, 'api_key': api_key}
    r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
    if r.status_code == 200:
        centroid = [r.json()['rows'][0]['lat'], r.json()['rows'][0]['lng']]
    else:
        centroid = None

    # Get speces
    q = "select distinct scientificname as species from point_uploads_master where datasetid='{0}' and scientificname is not null and scientificname !='' and decimalLatitude is not null and decimalLongitude is not null order by scientificname".format(datasetid)
    params = {'q': q, 'api_key': api_key}
    r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
    if r.status_code == 200:
        species = [x['species'] for x in r.json()['rows']]
    else:
        species = None
    
    return entries, title, centroid, species


def delete_dataset(current_user, datasetid):
    """Delete selected dataset."""
    
    email = current_user['email']
    
    # Check property of dataset
    q = "select count(*) as cont from point_uploads_registry where datasetid='{0}' and email='{1}'".format(datasetid, email)
    params = {'q': q, 'api_key': api_key}
    r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
    if r.status_code == 200:
        entries = r.json()['rows'][0]['cont']
    else:
        entries = None
    
    if entries == 1:
        
        # Delete point_uploads_XXX table
        q = "drop table point_uploads_{0}".format(datasetid.replace('-','_'))
        params = {'q': q, 'api_key': api_key}
        r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
        if r.status_code == 200:
            # Delete records from point_uploads_registry
            q = "delete from point_uploads_registry where datasetid='{0}'".format(datasetid)
            params = {'q': q, 'api_key': api_key}
            r = requests.get('http://mol.cartodb.com/api/v2/sql', params=params)
            if r.status_code == 200:
                success = True
            else:
                print r.json()
                success = False
        else:
            print r.json()
            success = False
    else:
        print r.json()
        success = False
    
    return success
