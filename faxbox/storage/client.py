import os

from google.cloud import storage
from google.oauth2.service_account import Credentials


class Client(object):

    def __init__(self, credentials=None):
        credentials = credentials or Client.load_credentials()
        self.client = storage.Client(project=os.environ.get('GCE_PROJECT_ID'), credentials=credentials)
        self.bucket = self.client.get_bucket('faxbox')

    @classmethod
    def load_credentials(cls):
        credentials = (Credentials.from_service_account_info({
            'type': os.environ.get('GCE_TYPE'),
            'project_id': os.environ.get('GCE_PROJECT_ID'),
            'private_key_id': os.environ.get('GCE_PRIVATE_KEY_ID'),
            'private_key': os.environ.get('GCE_PRIVATE_KEY').replace('\\n', '\n'),
            'client_email': os.environ.get('GCE_CLIENT_EMAIL'),
            'client_id': os.environ.get('GCE_CLIENT_ID'),
            'auth_uri': os.environ.get('GCE_AUTH_URI'),
            'token_uri': os.environ.get('GCE_TOKEN_URI'),
            'auth_provider_x509_cert_url': os.environ.get('GCE_AUTH_PROVIDER_X509_CERT_URL'),
            'client_x509_cert_url': os.environ.get('GCE_CLIENT_X509_CERT_URL'),
        }))

        return credentials

    def upload(self, filename, file):
        blob = self.bucket.blob(filename)
        blob.upload_from_file(file, size=file.tell())
        blob.make_public()
        return blob.public_url
