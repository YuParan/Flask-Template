import flask
from flask import Response

import flask_restful
from flask_restful import reqparse

app = flask.Flask(__name__)
api = flask_restful.Api(app)


def parsing(parsing_list):
    """ 파라미터의 데이터를 파싱합니다. 데이터는 단일 값이어야 합니다 (not list) """
    parser = reqparse.RequestParser()
    _ = [parser.add_argument(pl) for pl in parsing_list]
    args = parser.parse_args()
    return args


class ServerResponse(Response):
    def __init__(self, status_code, message, payload):
        super().__init__(
            status=status_code,
            response=flask.json.dumps({
                'code': status_code,
                'message': message,
                'payload': payload
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            content_type='application/json'
        )


class HealthCheck(flask_restful.Resource):
    def get(self):
        return ServerResponse(
            200,
            'server is Healthy.',
            {}
        )


class ReTurn(flask_restful.Resource):
    def get(self):
        parsing_list = ['item', 'count']
        args = parsing(parsing_list)
        return ServerResponse(
            200,
            "Response successful",
            args
        )


# APIs
api.add_resource(HealthCheck, '/health')
api.add_resource(ReTurn, '/return')

if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port="8888",
            debug=True)

# Run Server (CLI input)
# python single_file_server.py
