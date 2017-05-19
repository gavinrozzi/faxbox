

class Mail(object):

    def __init__(self, to='', to_name='', from_='', from_name='', subject='', body='', attachments=None):
        self.to = to
        self.to_name = to_name
        self.from_ = from_
        self.from_name = from_name
        self.subject = subject
        self.body = body
        self.attachments = attachments or []


class Attachment(object):

    def __init__(self, name='', url=''):
        self.name = name
        self.url = url
