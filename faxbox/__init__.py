import json

from flask import Response


class BadRequest(Response):

    def __init__(self, message, status=400):
        super(BadRequest, self).__init__(
            response=json.dumps({
                'status': status,
                'message': message
            }),
            status=status,
            content_type='application/json'
        )


class NotFound(Response):

    def __init__(self, message, status=404):
        super(NotFound, self).__init__(
            response=json.dumps({
                'status': status,
                'message': message
            }),
            status=status,
            content_type='application/json'
        )


class Success(Response):
    def __init__(self, response, status=201):
        super(Success, self).__init__(
            response=json.dumps(response),
            status=status,
            content_type='application/json'
        )
