import httpx
import os
import time
from typing import Optional, Dict, Any
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.domain.entities import ExternalApiResult

TIMEOUT = int(os.getenv("OPEN_LIBRARY_TIMEOUT", "10"))
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
CACHE_SIZE = int(os.getenv("CACHE_MAX_SIZE", "512"))
_cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)
BASE_URL = "https://openlibrary.org/search.json"


class OpenLibraryClient:
    async def lookup(self, isbn: Optional[str] = None, title: Optional[str] = None, author: Optional[str] = None) -> ExternalApiResult:
        cache_key = f"ol:{isbn or ''}{title or ''}{author or ''}"
        if cache_key in _cache:
            return ExternalApiResult.ok("open_library", _cache[cache_key], 0, cached=True)
        start = time.time()
        try:
            result = await self._fetch(isbn, title, author)
            latency = (time.time() - start) * 1000
            _cache[cache_key] = result
            return ExternalApiResult.ok("open_library", result, latency)
        except Exception as e:
            latency = (time.time() - start) * 1000
            return ExternalApiResult.fail("open_library", str(e), latency)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(httpx.RequestError),
    )
    async def _fetch(self, isbn, title, author) -> Dict[str, Any]:
        params = {}
        if isbn:
            params["isbn"] = isbn
        else:
            if title:
                params["title"] = title
            if author:
                params["author"] = author
        params["limit"] = 1
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(BASE_URL, params=params)
            r.raise_for_status()
            data = r.json()
        docs = data.get("docs", [])
        if not docs:
            raise ValueError("No results from Open Library")
        doc = docs[0]
        cover_id = doc.get("cover_i")
        return {
            "title": doc.get("title", ""),
            "authors": doc.get("author_name", []),
            "publisher": doc.get("publisher", [""])[0] if doc.get("publisher") else "",
            "description": "",
            "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else "",
            "publication_year": str(doc.get("first_publish_year", "")) if doc.get("first_publish_year") else None,
            "categories": doc.get("subject", [])[:3],
            "source": "open_library",
        }

    async def health_check(self) -> Dict[str, Any]:
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(BASE_URL, params={"q": "test", "limit": 1})
                r.raise_for_status()
            return {"status": "ok", "latency_ms": (time.time() - start) * 1000}
        except Exception as e:
            return {"status": "error", "latency_ms": (time.time() - start) * 1000, "error": str(e)}
