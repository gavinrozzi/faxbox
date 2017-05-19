import os
import requests

from faxbox.fax.client import Client as FaxClient
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
    return '', 202


@app.route('/StatusUpdate', methods=['POST'])
def status_update():
    print request.values
    return '', 202


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)