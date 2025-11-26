from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .ai_adapter import generate_summary
from .cache import get_cache
import time
import logging

router = APIRouter()
logger = logging.getLogger('app')

class TextPayload(BaseModel):
    text: str


@router.get('/health')
async def health():
    return JSONResponse(status_code=200, content={"status": "ok"})


@router.post('/ai/summarize')
async def ai_summarize(payload: TextPayload, request: Request):
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail='missing text')

    cache = get_cache()
    provider = 'mock'

    key = f"summ:{hash(payload.text)}:{provider}"
    start = time.time()
    cached = await cache.get(key)
    if cached:
        logger.info('ai.summarize', extra={"request_id": request.state.request_id, "cache_hit": True})
        return {"summary": cached, "cached": True}

    try:
        summary = await generate_summary(payload.text, {"provider": provider})
        await cache.set(key, summary, ttl=3600)
        elapsed = time.time() - start
        logger.info('ai.summarize', extra={"request_id": request.state.request_id, "cache_hit": False, "duration_ms": int(elapsed*1000)})
        return {"summary": summary, "cached": False}
    except Exception as e:
        logger.exception('ai.error', extra={"request_id": request.state.request_id})
        raise HTTPException(status_code=502, detail='ai_service_error')
