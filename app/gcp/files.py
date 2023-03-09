import os
from google.cloud import storage
from requests import request
from flask import current_app


gcs_scope = 'https://www.googleapis.com/auth/devstorage.read_write '\
    'https://www.googleapis.com/auth/devstorage.read_only '\
    'https://www.googleapis.com/auth/devstorage.full_control '\
    

key_file = current_app.config['SERVICE_ACCOUNT_KEY']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file

class CloudStorage:
    def __init__(self,bucket = None):
        self.storage_client = storage.Client()
        self.bucket = bucket
        
    def create_bucket(self,bucket_name):
        
        bucket = self.storage_client.bucket(bucket_name)
        bucket.location = 'US-EAST1'
        bucket.storage_class = "STANDARD" 
        self.storage_client.create_bucket(bucket)
        

    def delete_bucket(self):
        try:
            bucket_to_delete = self.storage_client.get_bucket(self.bucket)
            bucket_to_delete.delete()
        except Exception as e:
            print(e)

    def bucket_permissions(self,bucket_name):
        bucket = self.storage_client.bucket(bucket_name)
        policy = bucket.get_iam_policy(requested_policy_version=3)
        policy.bindings.append({"role": 'roles/storage.objectAdmin', "members": {'allUsers'}}) 
        bucket.set_iam_policy(policy)
        

    def upload_files(self,uploaded_file,name_of_file,generated=False):
          
        
        cloud_bucket = self.storage_client.bucket(self.bucket)
        blob = cloud_bucket.blob(name_of_file)

        if generated:
            blob.upload_from_file(uploaded_file, rewind=True)
        else:
            blob.upload_from_string(uploaded_file.read(),
                content_type=uploaded_file.content_type)
            
        
    def delete_files(self,name_of_file):
        
         
        cloud_bucket = self.storage_client.bucket(self.bucket)
        blob = cloud_bucket.blob(name_of_file)
        blob.delete()
            
    def move_files(self,name_of_file,new_bucket):
        cloud_bucket = self.storage_client.bucket(self.bucket)
        source_blob = cloud_bucket.blob(name_of_file)
        destination_bucket = self.storage_client.bucket(new_bucket)

        blob_copy = cloud_bucket.copy_blob(
            source_blob, destination_bucket, name_of_file
        )
        cloud_bucket.delete_blob(name_of_file)

    def rename_files(self,file_name, new_name):
    
        bucket = self.storage_client.bucket(self.bucket)
        blob = bucket.blob(file_name)

        bucket.rename_blob(blob, new_name)

