import os
import logging
import time
from datetime import datetime

import flask
from flask import Response
import flask_restful

try:
    import uwsgi
except ModuleNotFoundError:
    print("\n======== Use Flask Runserver settings ========\n")


logger = logging.getLogger(__name__)


class HealthCheck(flask_restful.Resource):
    def get(self):
        return Response(
            status=200,
            response=flask.json.dumps({
                'code': 200,
                'message': 'nameless_server is Healthy.',
                'payload': {
                    "server-time": str(datetime.now()),
                    "server_timezone": [
                        os.environ['TZ'],
                        time.tzname[0]
                    ]
                }
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            content_type='application/json'
        )


class Restart(flask_restful.Resource):
    def get(self):
        """ Flask Runserver 로 서버 구동 시, 해당 API 는 동작하지 않습니다 (uwsgi 사용) """
        try:
            uwsgi.reload()
            logger.info("Restart uWSGI Server")
            return Response(
                status=200,
                response=flask.json.dumps({
                    'code': 200,
                    'message': 'nameless_server is restarted successfully.',
                    'payload': {}
                }, sort_keys=True, indent=4, separators=(',', ': ')),
                content_type='application/json'
            )
        except NameError:
            return Response(
                status=200,
                response=flask.json.dumps({
                    'code': 200,
                    'message': 'Restart is not necessary in Flask Runserver settings',
                    'payload': {}
                }, sort_keys=True, indent=4, separators=(',', ': ')),
                content_type='application/json'
            )
