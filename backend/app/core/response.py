"""统一响应格式"""
from fastapi.responses import JSONResponse


class ResponseCode:
    SUCCESS = 0
    PARAM_ERROR = 1001
    UNAUTHORIZED = 1002
    FORBIDDEN = 1003
    NOT_FOUND = 1004
    SERVER_ERROR = 5000


def api_response(code: int = 0, msg: str = "success", data=None) -> JSONResponse:
    return JSONResponse(
        content={"code": code, "msg": msg, "data": data}
    )


def success_response(data=None, msg: str = "success") -> JSONResponse:
    return api_response(code=0, msg=msg, data=data)


def error_response(code: int, msg: str = "error", data=None) -> JSONResponse:
    return api_response(code=code, msg=msg, data=data)
