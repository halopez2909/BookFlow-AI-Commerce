import httpx
import os
import time
from typing import Optional, Dict, Any
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.domain.entities import ExternalApiResult

TIMEOUT = int(os.getenv("GOOGLE_BOOKS_TIMEOUT", "10"))
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
CACHE_SIZE = int(os.getenv("CACHE_MAX_SIZE", "512"))
_cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)
BASE_URL = "https://www.googleapis.com/books/v1/volumes"


class GoogleBooksClient:
    async def lookup(self, isbn: Optional[str] = None, title: Optional[str] = None, author: Optional[str] = None) -> ExternalApiResult:
        cache_key = f"gb:{isbn or ''}{title or ''}{author or ''}"
        if cache_key in _cache:
            return ExternalApiResult.ok("google_books", _cache[cache_key], 0, cached=True)
        start = time.time()
        try:
            result = await self._fetch(isbn, title, author)
            latency = (time.time() - start) * 1000
            _cache[cache_key] = result
            return ExternalApiResult.ok("google_books", result, latency)
        except Exception as e:
            latency = (time.time() - start) * 1000
            return ExternalApiResult.fail("google_books", str(e), latency)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(httpx.RequestError),
    )
    async def _fetch(self, isbn, title, author) -> Dict[str, Any]:
        query = f"isbn:{isbn}" if isbn else f"intitle:{title or ''} inauthor:{author or ''}"
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(BASE_URL, params={"q": query, "maxResults": 1})
            r.raise_for_status()
            data = r.json()
        items = data.get("items", [])
        if not items:
            raise ValueError("No results from Google Books")
        info = items[0].get("volumeInfo", {})
        image_links = info.get("imageLinks", {})
        return {
            "title": info.get("title", ""),
            "authors": info.get("authors", []),
            "publisher": info.get("publisher", ""),
            "description": info.get("description", ""),
            "cover_url": image_links.get("thumbnail", ""),
            "publication_year": info.get("publishedDate", "")[:4] if info.get("publishedDate") else None,
            "categories": info.get("categories", []),
            "source": "google_books",
        }

    async def health_check(self) -> Dict[str, Any]:
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(BASE_URL, params={"q": "test", "maxResults": 1})
                r.raise_for_status()
            return {"status": "ok", "latency_ms": (time.time() - start) * 1000}
        except Exception as e:
            return {"status": "error", "latency_ms": (time.time() - start) * 1000, "error": str(e)}
