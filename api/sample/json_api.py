import logging

import flask_restful
from flask_restful import reqparse

from api.response import Argument, NamelessServer_Response


logger = logging.getLogger(__name__)


class JsonAPI(flask_restful.Resource):
    """ Postman 을 활용해서 테스트를 진행할 경우, Request 전송방식을 raw(type=json) 으로 지정해줘야 합니다 """

    def post(self):
        """
        :action:
            application/json (raw) 형식으로 parameter 를 입력받아 내용을 파싱한 후, json 포맷으로 동일하게 응답합니다.
            Flask 에서 json Request 와 그 처리를 위한 예시 API 입니다.

        :param: request parameter
            "param0": (bool)
            "param1": (int)
            "param2": (float)
            "param3": (str)
            "param4": (dict)
            "param5": (list)
            "session": (str) 선택 파라미터 - default: "test_session"

            Test Json Raw
            {
                "param0": false,
                "param1": 5,
                "param2": 2.4,
                "param3": "flask",
                "param4": {
                    "arg1": 1,
                    "arg2": 2
                },
                "param5": [9, 8.8, {"s": 7}],
                "session": "test_session"
            }

        :return: response payload
            request parameter 와 동일한 값을 동일하게 응답합니다.
            "param0": (bool)
            "param1": (int)
            "param2": (float)
            "param3": (str)
            "param4": (dict)
            "param5": (list)
            "session": (str) 선택 파라미터 - default: "test_session"
        """
        # Parse Parameter  --  type 미 지정시, str 으로 입력됩니다.
        parser = reqparse.RequestParser(argument_class=Argument)
        parser.add_argument('param0', type=bool)  # '어떤 값이 존재하면' True 가 되므로 주의 (ex. "asdf" > True)
        parser.add_argument('param1', type=int)
        parser.add_argument('param2', type=float)
        parser.add_argument('param3', type=str)
        parser.add_argument('param4', type=dict)
        parser.add_argument('param5', type=list, location='json')  # list 형 입력의 경우, location="json" 지정 필수
        parser.add_argument('session', type=str, default="test_session")  # 선택 parameter 의 default 지정
        args = parser.parse_args()

        # 필수 Parameter Check
        required_parameters = ['param0', 'param1', 'param2', 'param3', 'param4', 'param5']
        if any(args[rq] is None for rq in required_parameters):
            logger.error(args)
            return NamelessServer_Response(
                400,
                "파라미터가 존재하지 않습니다",
                {}
            )

        # 최종 정상 응답
        return NamelessServer_Response(
            200,
            "파라미터를 정상적으로 파싱하였습니다.",
            {"args": args}
        )
