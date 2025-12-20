"""Logging middleware acts as a request/response logger and tracer."""

import time
import uuid
from typing import Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, _StreamingResponse

from app.core.logger import request_id_var


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        # Generate request ID for tracing
        request_id = str(uuid.uuid4())[:8]

        # Add request ID to request state
        request.state.request_id = request_id

        # Make request ID visible to the logger
        request_id_var.set(request_id)

        start_time = time.time()

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Log request with more details
        logger.info(
            f"Method[{request.method}] URL[{request.url.path}] | "
            f"Client[{client_ip}] | User-Agent[{request.headers.get('user-agent', 'unknown')}]",
            request_id=request_id,
        )

        try:
            response: _StreamingResponse = await call_next(request)

            # Log response
            process_time = time.time() - start_time
            logger.info(
                f"Method[{request.method}] URL[{request.url.path}] | " f"Status[{response.status_code}] | Process Time[{process_time:.3f}s]",
                request_id=request_id,
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            process_time = time.time() - start_time

            try:
                json_body = await request.json()
            except Exception:
                json_body = ""

            logger.error(
                f"Method[{request.method}] URL[{request.url.path}] | " f"Error Message[{str(e)}] | Process Time[{process_time:.3f}s]",
                request_body=json_body,
                request_query_params=request.query_params,
                request_path_params=request.path_params,
            )
            raise e
