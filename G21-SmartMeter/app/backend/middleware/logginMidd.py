from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class Log(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"[Middleware] percorso Richiesta: {request.url.path}")
        response = await call_next(request)
        print(f"[Middleware] stato Risposta: {response.status_code}")
        return response

