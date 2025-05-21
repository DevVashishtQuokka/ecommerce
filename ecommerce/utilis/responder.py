from rest_framework.response import Response
from rest_framework import status
from utils.consts import constants
class Responder:
    @staticmethod
    def success_response(code, data=None, status_code=status.HTTP_200_OK):
        res = {
            "code": code,
            "message": constants.get(code, "Success"),
            "data": data if data is not None else {}
        }
        return Response(res, status=status_code)

    @staticmethod
    def error_response(code, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        res = {
            "code": code,
            "message": constants.get(code, "An error occurred."),
        }
        if errors is not None:
            res["errors"] = errors
        return Response(res, status=status_code)
