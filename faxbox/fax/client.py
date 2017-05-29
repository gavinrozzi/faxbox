import os
import requests

from faxbox.fax import Fax
from twilio.rest import Client as Twilio

class Client(object):

    def __init__(self, username=None, password=None):
        self.username = username or os.environ.get('TWILIO_ACCOUNT_SID')
        self.password = password or os.environ.get('TWILIO_AUTH_TOKEN')

        self.client = Twilio(self.username, self.password)

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
        return Fax(
            fax.sid,
            fax.to,
            fax.from_,
            fax.media_url,
            fax.status
        )

    def create_fax_number(self, email):
        numbers = requests.get(
            'https://api.twilio.com/2010-04-01/Accounts/{}/AvailablePhoneNumbers/US/Local.json'.format(self.username),
            params={
                'FaxEnabled': True
            },
            auth=(self.username, self.password)
        )

        for number in numbers.json()['available_phone_numbers']:
            purchased_number = requests.post(
                'https://api.twilio.com/2010-04-01/Accounts/{}/IncomingPhoneNumbers.json'.format(self.username),
                data={
                    'FriendlyName': 'Fax number for {}'.format(email),
                    'PhoneNumber': number['phone_number'],
                    'VoiceReceiveMode': 'fax',
                    'VoiceUrl': 'http://www.faxbox.email/api/v1/receive',
                    'VoiceMethod': 'POST',
                },
                auth=(self.username, self.password)
            )
            return purchased_number.json()['phone_number']
