"""
FastAPI Calculator application.

Serves a small web UI at "/" and exposes JSON endpoints for the four basic
arithmetic operations: /add, /subtract, /multiply and /divide.
"""

import logging

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator

from app.logging_config import setup_logging
from app.operations import add, divide, multiply, subtract

setup_logging()
logger = logging.getLogger("calculator")

app = FastAPI(title="FastAPI Calculator")
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b", mode="before")
    @classmethod
    def validate_numbers(cls, value):
        # Reject booleans and strings: only real numbers are accepted.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("HTTPException on %s: %s", request.url.path, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = "; ".join(f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors())
    logger.error("Validation error on %s: %s", request.url.path, messages)
    return JSONResponse(status_code=400, content={"error": messages})


# ---------------------------------------------------------------------------
# Middleware: log every request
# ---------------------------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Request: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info(
        "Response: %s %s -> %s", request.method, request.url.path, response.status_code
    )
    return response


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
async def read_root(request: Request):
    """Serve the calculator page."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
async def health():
    """Simple health check used by the E2E test server fixture."""
    return {"status": "ok"}


def _run(op_name: str, func, operation: OperationRequest) -> OperationResponse:
    """Run an operation, log it and convert unexpected errors to HTTP 400/500."""
    try:
        result = func(operation.a, operation.b)
        logger.info("%s(%s, %s) = %s", op_name, operation.a, operation.b, result)
        return OperationResponse(result=result)
    except ValueError as exc:
        logger.error("%s error: %s", op_name, exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # pragma: no cover - safety net
        logger.exception("Unexpected error in %s", op_name)
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    return _run("add", add, operation)


@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    return _run("subtract", subtract, operation)


@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    return _run("multiply", multiply, operation)


@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    return _run("divide", divide, operation)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
