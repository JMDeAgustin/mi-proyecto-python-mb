from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from loguru import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP {exc.status_code} ({request.url.path}): {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error in {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
