import cloudstorage as gcs

class GoogleCloudStorage():
    """."""
    
    def __init__(self, project_id, bucket_name):
        
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.bucket = '/' + bucket_name
        return
    
    def create_file(self, filename, content="Sample content"):
        """Create a new file in the bucket with the given name and content."""
        filepath = self.bucket + '/' + filename
        gcs_file = gcs.open(filepath, 'w', content_type='text/plain',
                            #options={'x-goog-project-id': self.project_id}
                            )
        gcs_file.write(content)
        gcs_file.close()
        return
    
    def open_file(self, filename):
        """Returns an open file-like object with the content of the file to be read. DO NOT FORGET TO CLOSE!"""
        filepath = self.bucket + '/' + filename
        gcs_file = gcs.open(filepath)
        return gcs_file
        
    
    def stat_file(self, filename):
        """."""
        filepath = self.bucket + '/' + filename
        stat = gcs.stat(filepath)
        return repr(stat)
    
    def delete_file(self, filename):
        """Deletes the file from CloudStorage."""
        filepath = self.bucket + '/' + filename
        try:
            gcs.delete(filepath)
        except gcs.NotFoundError:
            pass
        return

    def list_bucket(self):
        """Returns a list of files currently available in the bucket."""
        stats = gcs.listbucket(self.bucket)
        files = [x.filename for x in stats]
        return files
    
    def empty_bucket(self):
        """Delete all elements in bucket."""
        for i in self.list_bucket():
            gcs.delete(i)
        return
    
    
