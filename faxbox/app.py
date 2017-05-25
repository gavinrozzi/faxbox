import os

from faxbox.fax.client import Client as FaxClient
from faxbox.mail import Mail, Attachment
from faxbox.mail.client import Client as EmailClient
from faxbox.storage.client import Client as StorageClient
from flask import Flask, request

app = Flask(__name__)
fax_client = FaxClient()
email_client = EmailClient()
storage_client = StorageClient()


@app.route('/')
def index():
    return 'faxbox', 200


@app.route('/api/v1/email', methods=['POST'])
def email():
    if 'attachment1' not in request.files:
        return 'No attachment found', 400

    file = request.files['attachment1']
    public_url = storage_client.upload('fax.pdf', file)

    fax_sid = fax_client.send_fax(
        'FROM',
        'TO',
        public_url,
        status_callback='CALLBACK'
    )

    return 'Saved', 202


@app.route('/api/v1/register', methods=['POST'])
def register():

    return ''


@app.route('/api/v1/receive', methods=['POST'])
def fax():
    print request.values
    return '', 202


@app.route('/api/v1/callback', methods=['GET', 'POST'])
def callback():
    if 'OriginalMediaUrl' in request.values:
        sender = request.values.get('From')
        mail = Mail(
            to='TO',
            from_='f{}@faxbox.com'.format(sender),
            from_name=sender,
            subject='Fax from {}!'.format(sender),
            body='You\'ve received the attached fax from {}'.format(sender),
            attachments=[
                Attachment(
                    'fax.pdf',
                    request.values.get('OriginalMediaUrl')
                )
            ]
        )
        email_client.send_email(mail)
        return '', 200

    return '', 204


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)