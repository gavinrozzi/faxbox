import datetime
import json
import os

from faxbox import BadRequest, Success, NotFound
from faxbox.db.client import Client as DbClient
from faxbox.fax.client import Client as FaxClient
from faxbox.mail import Mail, Attachment
from faxbox.mail.client import Client as EmailClient
from faxbox.storage.client import Client as StorageClient
from flask import Flask, request
from time import sleep

app = Flask(__name__, static_url_path='/static')
fax_client = FaxClient()
email_client = EmailClient()
storage_client = StorageClient()
db_client = DbClient()


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html'), 200


@app.route('/api/v1/email', methods=['POST'])
def email():
    if 'attachment1' not in request.files:
        return BadRequest('No attachment found.')

    if 'envelope' not in request.values:
        return BadRequest('Missing parameter `envelope`.')

    if 'to' not in request.values:
        return BadRequest('Missing parameter `to`.')

    envelope = json.loads(request.values.get('envelope'))
    from_user = db_client.fetch_user_by_email(envelope['from'])
    from_number =  os.environ.get('DEFAULT_FAX_NUMBER') if from_user is None else from_user.number
    to_number = request.values.get('to').replace('@mail.faxbox.email', '')[1:]

    public_url = storage_client.upload(
        '{}-{}-{}.pdf'.format(from_number, to_number, datetime.datetime.now().isoformat()),
        request.files['attachment1']
    )

    fax_sid = fax_client.send_fax(to_number, from_number, public_url)
    return Success({
        'fax_sid': fax_sid,
        'from': from_number,
        'to': to_number,
        'media_url': public_url
    }, status=201)


@app.route('/api/v1/register', methods=['POST'])
def register():
    if 'name' not in request.values:
        return BadRequest('Missing parameter `name`.')

    if 'email' not in request.values:
        return BadRequest('Missing parameter `email`.')

    try:

        number = fax_client.create_fax_number(request.values.get('email'))
        db_client.add_user(request.values.get('name'), request.values.get('email'), number)

        return Success({
            'name': request.values.get('name'),
            'email': request.values.get('email'),
            'number': number
        }, status=201)

    except Exception:
        return BadRequest('Failed to add user.')


@app.route('/api/v1/sent', methods=['POST'])
def fax_sent():
    return """
        <Response>
            <Receive action="/api/v1/receive"/>
        </Response>
    """, 200


@app.route('/api/v1/receive', methods=['POST'])
def receive():
    if 'MediaUrl' not in request.values:
        return BadRequest('Missing parameter `MediaUrl`.')

    sender = request.values.get('From')
    user = db_client.fetch_user_by_number(request.values.get('To'))
    if not user:
        return NotFound('No email found for {}.'.format(request.values.get('To')))

    mail = Mail(
        to=user.email,
        from_='f{}@mail.faxbox.email'.format(sender),
        from_name=sender,
        subject='Fax from {}!'.format(sender),
        body='You\'ve received the attached fax from {}'.format(sender),
        attachments=[
            Attachment(
                'fax.pdf',
                request.values.get('MediaUrl')
            )
        ]
    )
    email_client.send_email(mail)
    return Success({
        'to': user.email,
        'from': 'f{}@mail.faxbox.email'.format(sender),
        'media_url': request.values.get('MediaUrl')
    }, status=201)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)