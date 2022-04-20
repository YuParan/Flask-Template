import logging

import flask_restful
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

from api.response import Argument, NamelessServer_Response

from PIL import Image
import pandas as pd


logger = logging.getLogger(__name__)


class UploadFormData(flask_restful.Resource):
    """ Postman 을 활용해서 테스트를 진행할 경우, Request 전송방식을 form-data 로 지정해줘야 합니다
        text 를 받는 경우, key(type=text) , File 이 입력되는 경우 key(type=file) 로 지정해줘야 합니다
        테스트용 Image & CSV 파일 처리를 위해, Pillow, Pandas 라이브러리가 필요합니다 """

    def post(self):
        """
        :action:
            form-data 형식으로 parameter 와 file 을 입력받아, 업로드 된 file 의 내부 정보를 응답합니다.
            Flask 에서 파일 Request 와 그 처리를 위한 예시 API 입니다.

        :param: request parameter
            "is_save": (int) 업로드 된 파일의 저장 여부. 0 or 1
                        ! 주의 ! : form-data 형식의 경우, 모든 파라미터는 str 타입으로 파싱합니다.
            "image": (file) Image File
            "dataframe": (file) CSV File

        :return: response payload
            "is_save": (bool) 업로드 된 파일의 저장 여부
            "image": {
                "width": (int) 업로드 된 이미지의 가로 픽셀
                "height": (int) 업로드 된 이미지의 세로 픽셀
            },
            "dataframe": {
                "columns": (list) 업로드 된 dataframe 의 columns
                "length": (int) 업로드 된 csv dataframe 의 전체 데이터 길이
        """
        # Parse Parameter  --  type 미 지정시, str 으로 입력됩니다.
        parser = reqparse.RequestParser(argument_class=Argument)
        parser.add_argument('is_save', type=int, default=0)  # Save True=1 / False=0
        parser.add_argument('image', type=FileStorage, location="files")
        parser.add_argument('dataframe', type=FileStorage, location="files")
        args = parser.parse_args()

        # 필수 Parameter Check
        required_parameters = ['is_save', 'image', 'dataframe']
        if any(args[rq] is None for rq in required_parameters):
            logger.error(args)
            return NamelessServer_Response(
                400,
                "파라미터가 존재하지 않습니다",
                {}
            )

        # 'is_save' Parameter Type Check
        if args['is_save'] == 0 or args['is_save'] == 1:
            args['is_save'] = bool(args['is_save'])
        else:
            return NamelessServer_Response(
                400,
                f"Boolean 처리 할 수 없는 파라미터 입니다. 0 또는 1 값이여야 합니다. input: {args['is_save']}",
                {}
            )

        image = Image.open(args['image'])  # type : PIL.Image
        dataframe = pd.read_csv(args['dataframe'])  # type : pandas.DataFrame

        if args['is_save']:
            image.save("save.png")
            dataframe.to_csv("save.csv")
            logger.info("Save Files")

        # 최종 정상 응답
        return NamelessServer_Response(
            200,
            "파일과 파라미터를 정상적으로 처리하였습니다.",
            {
                "is_save": args['is_save'],
                "image": {
                    "width": image.size[0],
                    "height": image.size[1]
                },
                "dataframe": {
                    "columns": dataframe.columns.tolist(),
                    "length": len(dataframe)
                }
            }
        )
