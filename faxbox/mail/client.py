import os
from base64 import b64encode

import requests
from sendgrid import SendGridAPIClient, Email
from sendgrid.helpers.mail import Mail, Content, Attachment


class Client(object):

    def __init__(self, secret=None):
        _secret = secret or os.environ.get('SENDGRID_API_KEY')

        self.client = SendGridAPIClient(apikey=_secret).client.mail.send

    def send_email(self, email):
        mail = Mail(
            to_email=Email(email.to, email.to_name),
            from_email=Email(email.from_, email.from_name),
            subject=email.subject,
            content=Content("text/plain", email.body)
        )

        for a in email.attachments:
            attachment = Attachment()
            attachment.filename = a.name
            attachment.content = self.url_content(a.url)

            mail.add_attachment(attachment)

        self.client.post(request_body=mail.get())

    def url_content(self, url):
        response = requests.get(url)
        return b64encode(response.content).decode()