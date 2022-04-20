import logging

import flask_restful
from flask_restful import reqparse

from api.response import Argument, NamelessServer_Response


logger = logging.getLogger(__name__)


class GetQueryString(flask_restful.Resource):
    """ Postman 을 활용해서 테스트를 진행할 경우, Get param 의 Key-Value 쌍을 작성해야 합니다 """

    def get(self):
        """
        :action:
            Django 에서 GET Request 와 그 처리를 위한 예시 API 입니다.
            GET 형식으로 parameter 를 입력받아 내용을 파싱한 후, json 포맷으로 동일하게 응답합니다.
        :param: request parameter
            "session": (str) 선택 파라미터 - default: "test_session"
            "query": (str)
            "lucky_number": (int)
        :return: response payload
            "get_parameters": (dict)
                {
                    "session": (str) 선택 파라미터 - default: "test_session"
                    "query": (str)
                    "lucky_number": (int)
                }
            "return_message": (str)
                f"{session} 님의 질문 사항은 {query} 네요. \n 질문에 답을 드리진 못하지만, 대신 행운의 숫자 {lucky_number} 를 드리겠습니다!"
        """
        # Parse Parameter  --  type 미 지정시, str 으로 입력됩니다.
        parser = reqparse.RequestParser(argument_class=Argument)
        parser.add_argument("session", type=str, default="test_session")  # 선택 parameter 의 default 지정
        parser.add_argument("query", type=str)
        parser.add_argument("lucky_number", type=int)
        args = parser.parse_args()

        # 필수 Parameter Check
        required_parameters = ['query', 'lucky_number']
        if any(args[rq] is None for rq in required_parameters):
            logger.error(args)
            return NamelessServer_Response(
                400,
                "파라미터가 존재하지 않습니다",
                {}
            )

        # 숫자 type 변환 체크
        try:
            args["lucky_number"] = int(args["lucky_number"])
        except Exception as e:
            logger.error(e)
            return NamelessServer_Response(
                400,
                f"lucky_number 파라미터는 정수(int) 변환 가능한 값이어야 합니다. input 'lucky_number': {args['lucky_number']}",
                {}
            )

        # 최종 정상 응답
        return NamelessServer_Response(
            200,
            "파라미터를 정상적으로 파싱하였습니다.",
            {
                "get_parameters": args,
                "return_message": f"{args['session']} 님의 질문 사항은 '{args['query']}' 네요. \n "
                                  f"질문에 답을 드리진 못하지만, 대신 행운의 숫자 [{args['lucky_number']}] 를 드리겠습니다!"
            }
        )
