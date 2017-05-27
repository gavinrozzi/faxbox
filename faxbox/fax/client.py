import os
import requests

from faxbox.fax import Fax
from twilio.rest import Client as Twilio

class Client(object):

    def __init__(self, username=None, password=None):
        _username = username or os.environ.get('TWILIO_ACCOUNT_SID')
        _password = password or os.environ.get('TWILIO_AUTH_TOKEN')

        self.client = Twilio(_username, _password)

    def send_fax(self, to, from_, media_url, status_callback=None):
        fax = self.client.fax.faxes.create(
            from_,
            to,
            media_url,
            status_callback=status_callback,
        )

        return fax.sid

    def get_fax(self, fax_sid):
        fax = self.client.fax.faxes.get(fax_sid).fetch()
        data = requests.get(fax.media_url)

        return Fax(
            fax.sid,
            fax.to,
            fax.from_,
            data.content
        )
