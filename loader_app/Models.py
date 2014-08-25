__author__ = '@jotegui'

from google.appengine.ext import ndb

class UploadedFile(ndb.Model):
    """Model for the CSV file storage."""
    uuid = ndb.StringProperty()
    name = ndb.StringProperty()
    content = ndb.BlobProperty()
