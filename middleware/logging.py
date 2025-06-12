import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from loguru import logger


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response: Response = await call_next(request)
        duration_ms = int((time.time() - start) * 1000)

        logger.info(
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} ({duration_ms} ms)"
        )
        return response
