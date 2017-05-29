import datetime
import json
import os
from time import sleep

from faxbox.db.client import Client as DbClient
from faxbox.fax.client import Client as FaxClient
from faxbox.mail import Mail, Attachment
from faxbox.mail.client import Client as EmailClient
from faxbox.storage.client import Client as StorageClient
from flask import Flask, request

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
        return 'No attachment found', 400

    if 'from' not in request.values:
        return 'Missing parameter from', 400

    if 'to' not in request.values:
        return 'Missing parameter to', 400

    from_ = request.values.get('from')
    to = request.values.get('to')

    from_user = db_client.fetch_user_by_email(from_)
    from_number =  os.environ.get('DEFAULT_FAX_NUMBER') if from_user is None else from_user.number
    to_number = to.replace('@mail.faxbox.email', '')[1:]

    file = request.files['attachment1']
    filename = '{}-{}-{}.pdf'.format(from_number, to_number, datetime.datetime.now().isoformat())
    public_url = storage_client.upload(filename, file)
    fax_sid = fax_client.send_fax(
        to_number,
        from_number,
        public_url
    )

    return fax_sid, 202


@app.route('/api/v1/register', methods=['POST'])
def register():
    if 'name' not in request.values:
        return 'Missing parameter name', 400

    if 'email' not in request.values:
        return 'Missing parameter email', 400

    number = fax_client.create_fax_number(request.values.get('email'))
    try:
        db_client.add_user(request.values.get('name'), request.values.get('email'), number)
    except Exception:
        return 'Failed to add user', 400

    return json.dumps({
        'name': request.values.get('name'),
        'email': request.values.get('email'),
        'number': number
    }), 201


@app.route('/api/v1/receive', methods=['POST'])
def receive():
    if 'FaxSid' not in request.values:
        return 'No fax sid provided', 400

    sender = request.values.get('From')
    user = db_client.fetch_user_by_number(request.values.get('To'))
    if not user:
        return 'Could not send email', 400

    fax = fax_client.get_fax(request.values.get('FaxSid'))
    while not fax or not fax.media_url:
        sleep(5)
        fax = fax_client.get_fax(request.values.get('FaxSid'))

        if fax.status == 'failed':
            return 'Failed to receive fax', 400

    mail = Mail(
        to=user.email,
        from_='f{}@faxbox.com'.format(sender),
        from_name=sender,
        subject='Fax from {}!'.format(sender),
        body='You\'ve received the attached fax from {}'.format(sender),
        attachments=[
            Attachment(
                'fax.pdf',
                fax.media_url
            )
        ]
    )
    email_client.send_email(mail)
    return '', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)