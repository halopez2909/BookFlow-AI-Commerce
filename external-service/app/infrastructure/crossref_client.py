import httpx
import os
import time
from typing import Optional, Dict, Any
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.domain.entities import ExternalApiResult

TIMEOUT = int(os.getenv("CROSSREF_TIMEOUT", "10"))
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
_cache = TTLCache(maxsize=256, ttl=CACHE_TTL)
BASE_URL = "https://api.crossref.org/works"


class CrossrefClient:
    async def lookup_by_issn(self, issn: str) -> ExternalApiResult:
        cache_key = f"cr:{issn}"
        if cache_key in _cache:
            return ExternalApiResult.ok("crossref", _cache[cache_key], 0, cached=True)
        start = time.time()
        try:
            result = await self._fetch(issn)
            latency = (time.time() - start) * 1000
            _cache[cache_key] = result
            return ExternalApiResult.ok("crossref", result, latency)
        except Exception as e:
            latency = (time.time() - start) * 1000
            return ExternalApiResult.fail("crossref", str(e), latency)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(httpx.RequestError),
    )
    async def _fetch(self, issn: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(BASE_URL, params={"filter": f"issn:{issn}", "rows": 1})
            r.raise_for_status()
            data = r.json()
        items = data.get("message", {}).get("items", [])
        if not items:
            raise ValueError(f"No results from Crossref for ISSN {issn}")
        item = items[0]
        authors = item.get("author", [])
        author_names = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors]
        return {
            "title": item.get("title", [""])[0] if item.get("title") else "",
            "authors": author_names,
            "publisher": item.get("publisher", ""),
            "description": item.get("abstract", ""),
            "publication_year": str(item.get("published", {}).get("date-parts", [[None]])[0][0] or ""),
            "issn": issn,
            "source": "crossref",
        }

    async def health_check(self) -> Dict[str, Any]:
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get("https://api.crossref.org/works", params={"rows": 1})
                r.raise_for_status()
            return {"status": "ok", "latency_ms": (time.time() - start) * 1000}
        except Exception as e:
            return {"status": "error", "latency_ms": (time.time() - start) * 1000, "error": str(e)}
