import six
import logging

import flask
from flask import current_app, Response
import flask_restful
from flask_restful import reqparse


logger = logging.getLogger(__name__)


class Argument(reqparse.Argument):
    """
    Override reqparse.Argument :
        flask_restful.abort(400, message=msg) -> flask_restful.abort(ServerResponse(...))
    add_argument 로 parameter 파싱 시, 지정한 parameter Type 과 다른 경우 ,
    지정된 Server_Response 와 동일한 형태의 Response 를 자동으로 보내도록 Override
    """

    def handle_validation_error(self, error, bundle_errors):
        """Called when an error is raised while parsing. Aborts the request
        with a 400 status and an error message

        :param error: the error that was raised
        :param bundle_errors: do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg
        # Custom Type-Error Message
        logger.error(f" {self.name} - {error_msg} ")
        flask_restful.abort(
            NamelessServer_Response(400, f" {self.name} - {error_msg} ", {})
        )


class GeneralResponse:
    """ GeneralResponse Class
    General definition of API Response
    """

    def __init__(self, status_code, message, payload):
        """
        Params:
            code: HTTP status code
            message: Response message
            payload: Response data
        """
        self.response = flask.json.dumps({
            'code': status_code,
            'message': message,
            'payload': payload
        }, sort_keys=True, indent=4, separators=(',', ': '))

    def __repr__(self):
        return repr(self.response)


# TODO: 프로젝트의 이름에 따라 Response class (NamelessServer_Response) 의 이름 변경 필요
class NamelessServer_Response(Response):
    def __init__(self, status_code, message, payload):
        super().__init__(
            status=status_code,
            response=GeneralResponse(status_code, message, payload).response,
            content_type='application/json'
        )
