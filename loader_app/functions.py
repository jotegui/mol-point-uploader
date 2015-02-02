__author__ = '@jotegui'

from cartodb_apikey import api_key
import requests

def delete_dataset(current_user, datasetid):
    
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
