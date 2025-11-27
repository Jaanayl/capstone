from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .routes import router as api_router
from .logging_config import configure_logging
import os

configure_logging()

app = FastAPI()
app.include_router(api_router)


@app.middleware('http')
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get('X-Request-ID') or request.headers.get('x-request-id') or os.urandom(8).hex()
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": "internal_server_error", "request_id": getattr(request.state, 'request_id', None)})
