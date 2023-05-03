from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from main import app

class NotExistInListException(Exception) :
    def __init__(self, message: str):
        self.message = message

class NotInBoundException(Exception) :
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

@app.exception_handler(NotExistInListException)
async def not_exist_exception_handler(request: Request, exc: NotExistInListException):
    return JSONResponse(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        content=jsonable_encoder({
            "url": request.url.path,
            "message": exc.message,
        }),
    )

@app.exception_handler(NotInBoundException)
async def not_in_bound_exception_handler(request: Request, exc: NotInBoundException):
    return JSONResponse(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        content=jsonable_encoder({
            "url": request.url.path,
            "message": exc.message,
        }),
    )