from fastapi.responses import JSONResponse

def error_response(message: str, code: int):
    response = {
        "result": {
            "status": "error",
            "message": message
        }
    }
    return JSONResponse(content=response, status_code=code)

def success_response(message: str, code: int):
    response = {
        "result": {
            "status": "success",
            "message": message
        }
    }
    return JSONResponse(content=response, status_code=code)