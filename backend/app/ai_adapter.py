import asyncio
import os
import re

async def _mock_summarize(text, settings):
    # naive: split sentences and return five most informative (longest)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    ranked = sorted(sentences, key=lambda s: -len(s))
    top = ranked[:5]
    return '\n'.join([s.strip() for s in top])


def _anonymize(text: str) -> str:
    # remove emails and phone-like numbers as quick PII guard
    text = re.sub(r"[\w\.-]+@[\w\.-]+", "[REDACTED]", text)
    text = re.sub(r"\+?\d[\d\-\s]{6,}\d", "[REDACTED]", text)
    return text

async def generate_summary(text: str, settings: dict) -> str:
    provider = os.getenv('LLM_PROVIDER', settings.get('provider', 'mock'))
    sanitized = _anonymize(text)
    if provider == 'mock':
        return await _mock_summarize(sanitized, settings)

    # TODO: implement adapters for azure/openrouter/vertex using env vars
    # keep a default graceful fallback
    return await _mock_summarize(sanitized, settings)
