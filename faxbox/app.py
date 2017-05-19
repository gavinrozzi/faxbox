import os

from faxbox.fax.client import Client as FaxClient
from faxbox.mail import Mail, Attachment
from faxbox.mail.client import Client as EmailClient
from flask import Flask, request

app = Flask(__name__)
fax_client = FaxClient()
email_client = EmailClient()

@app.route('/register', methods=['POST'])
def register():



    return ''


@app.route('/ReceiveFax', methods=['POST'])
def receive_fax():
    print request.values
    return '', 202


@app.route('/StatusCallback', methods=['GET', 'POST'])
def status_update():
    if 'OriginalMediaUrl' in request.values:
        sender = request.values.get('From')
        mail = Mail(
            to='niu@jingming.ca',
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