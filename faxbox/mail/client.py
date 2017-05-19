import os
from base64 import b64encode

from sendgrid import SendGridAPIClient, Email
from sendgrid.helpers.mail import Mail, Content, Attachment


class Client(object):

    def __init__(self, secret=None):
        _secret = secret or os.environ.get('SENDGRID_API_KEY')

        self.client = SendGridAPIClient(apikey=_secret).client.mail.send


    def send_email(self, to, from_, subject, body, attachments=None):
        attachments = attachments or []

        print 'hello there'

        mail = Mail(
            to_email=Email(to),
            from_email=Email(from_),
            subject=subject,
            content=Content("text/plain", "Hello, Email!")
        )

        for content in attachments:
            attachment = Attachment()
            attachment.filename = 'fax.pdf'
            attachment.content = b64encode(content).decode()

            mail.add_attachment(attachment)

        response = self.client.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
