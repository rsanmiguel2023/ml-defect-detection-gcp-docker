"""
Observability utilities for API logging and request tracing.
"""

import json
import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("ml_defect_detection")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)


def log_json(event: str, **kwargs):
    payload = {
        "event": event,
        **kwargs,
    }

    logger.info(json.dumps(payload))


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.perf_counter()

        try:
            response = await call_next(request)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            log_json(
                "request_completed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                latency_ms=latency_ms,
            )

            response.headers["X-Request-ID"] = request_id
            return response

        except Exception as error:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            log_json(
                "request_failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                latency_ms=latency_ms,
                error=str(error),
            )

            raise
