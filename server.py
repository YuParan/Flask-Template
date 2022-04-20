import os
from logging.config import dictConfig

import flask
import flask_restful

from nameless_server import settings, system_api
from api.sample import get_query_string, json_api, upload_form_data


class FlaskServer:
    def __init__(self):
        # Flask Server Setting
        self.app = flask.Flask(__name__)  # APP Name from __main__(=server name)
        self.api = flask_restful.Api(self.app)

        self.BASE_DIR = settings.BASE_DIR
        self.ENVIRONMENT = settings.ENVIRONMENT
        self.KEYS = settings.KEYS

        # TIMEZONE Setting
        os.environ['TZ'] = self.ENVIRONMENT['settings']['timezone']

        # Logger Setting
        dictConfig(settings.LOGGER_CONFIG)
        self.logger = self.app.logger
        self.logger.info(f"Initialize [ {self.app.name} ] Flask Server")


SERVER = FlaskServer()

app = SERVER.app
api = SERVER.api


# Flask Server API-URLs
# System APIs
api.add_resource(system_api.HealthCheck, '/health')
api.add_resource(system_api.Restart, '/restart')  # Work on uWSGI Runserver

# Test-Sample APIs
api.add_resource(get_query_string.GetQueryString, '/api/sample/get_query_string')
api.add_resource(json_api.JsonAPI,                '/api/sample/json_api')
api.add_resource(upload_form_data.UploadFormData, '/api/sample/upload_form_data')


# Runserver
if __name__ == '__main__':
    # python server.py 로 직접 실행 시 테스트 서버(debug=True)로 동작합니다
    environment = settings.ENVIRONMENT
    app.run(host=environment['server']['host'],
            port=environment['server']['port'],
            debug=True)
