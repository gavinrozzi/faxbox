import os

from google.cloud import storage

class Client(object):

    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket('faxbox')

    def upload(self, filename, file):
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file, size=file.tell())
        blob.make_public()
        return blob.public_url
