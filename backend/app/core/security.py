"""
Security utilities — rate limiting headers, input sanitisation helpers.
No authentication required (free public API), but connections are secured
via HTTPS redirect (in production) and strict CORS.
"""

import re

from fastapi import Request
from fastapi.responses import JSONResponse


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Strip dangerous characters and enforce a max length."""
    value = value.strip()
    value = re.sub(r"[<>\"'%;()&+]", "", value)
    return value[:max_length]


async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return response
