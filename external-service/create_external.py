import os

reqs = """fastapi==0.111.0
uvicorn==0.29.0
pydantic[email]==2.7.1
python-dotenv==1.0.1
httpx==0.27.0
tenacity==8.2.3
cachetools==5.3.3
pytest==8.2.0
pytest-mock==3.14.0
pytest-asyncio==0.23.6
"""

env = """GOOGLE_BOOKS_TIMEOUT=10
OPEN_LIBRARY_TIMEOUT=10
CROSSREF_TIMEOUT=10
EBAY_APP_ID=
CACHE_TTL_SECONDS=3600
CACHE_MAX_SIZE=512
SERVICE_PORT=8009
"""

env_example = """GOOGLE_BOOKS_TIMEOUT=10
OPEN_LIBRARY_TIMEOUT=10
CROSSREF_TIMEOUT=10
EBAY_APP_ID=your_ebay_app_id
CACHE_TTL_SECONDS=3600
CACHE_MAX_SIZE=512
SERVICE_PORT=8009
"""

entities = """from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class ExternalApiResult:
    source: str
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    latency_ms: float
    cached: bool = False

    @staticmethod
    def ok(source: str, data: Dict[str, Any], latency_ms: float, cached: bool = False) -> "ExternalApiResult":
        return ExternalApiResult(source=source, success=True, data=data, error=None, latency_ms=latency_ms, cached=cached)

    @staticmethod
    def fail(source: str, error: str, latency_ms: float) -> "ExternalApiResult":
        return ExternalApiResult(source=source, success=False, data=None, error=error, latency_ms=latency_ms)


@dataclass
class ApiHealthStatus:
    name: str
    status: str
    latency_ms: float
    last_checked: datetime
    error: Optional[str] = None
"""

schemas = """from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class BookLookupRequest(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    issn: Optional[str] = None


class ExternalApiResultResponse(BaseModel):
    source: str
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    latency_ms: float
    cached: bool


class ApiHealthResponse(BaseModel):
    name: str
    status: str
    latency_ms: float
    last_checked: datetime
    error: Optional[str] = None


class ExternalHealthResponse(BaseModel):
    overall: str
    apis: List[ApiHealthResponse]
"""

google_books = """import httpx
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
"""

open_library = """import httpx
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
"""

crossref = """import httpx
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
"""

use_cases = """from typing import Optional, List
from datetime import datetime
from app.domain.entities import ExternalApiResult, ApiHealthStatus
from app.domain.schemas import BookLookupRequest
from app.infrastructure.google_books_client import GoogleBooksClient
from app.infrastructure.open_library_client import OpenLibraryClient
from app.infrastructure.crossref_client import CrossrefClient


class LookupBookExternal:
    def __init__(self):
        self.google = GoogleBooksClient()
        self.open_library = OpenLibraryClient()
        self.crossref = CrossrefClient()

    async def execute(self, request: BookLookupRequest) -> ExternalApiResult:
        # Try Google Books first
        result = await self.google.lookup(request.isbn, request.title, request.author)
        if result.success:
            return result

        # Fallback to Open Library
        result = await self.open_library.lookup(request.isbn, request.title, request.author)
        if result.success:
            return result

        # Fallback to Crossref if ISSN provided
        if request.issn:
            result = await self.crossref.lookup_by_issn(request.issn)
            if result.success:
                return result

        # Final fallback
        return ExternalApiResult.fail(
            source="all_sources",
            error="No external source returned results",
            latency_ms=0,
        )


class CheckExternalHealth:
    def __init__(self):
        self.google = GoogleBooksClient()
        self.open_library = OpenLibraryClient()
        self.crossref = CrossrefClient()

    async def execute(self) -> List[ApiHealthStatus]:
        results = []
        now = datetime.utcnow()

        gb = await self.google.health_check()
        results.append(ApiHealthStatus(
            name="google_books", status=gb["status"],
            latency_ms=gb["latency_ms"], last_checked=now,
            error=gb.get("error"),
        ))

        ol = await self.open_library.health_check()
        results.append(ApiHealthStatus(
            name="open_library", status=ol["status"],
            latency_ms=ol["latency_ms"], last_checked=now,
            error=ol.get("error"),
        ))

        cr = await self.crossref.health_check()
        results.append(ApiHealthStatus(
            name="crossref", status=cr["status"],
            latency_ms=cr["latency_ms"], last_checked=now,
            error=cr.get("error"),
        ))

        return results
"""

router = """from fastapi import APIRouter, HTTPException
from app.domain.schemas import BookLookupRequest, ExternalApiResultResponse, ExternalHealthResponse, ApiHealthResponse
from app.application.use_cases import LookupBookExternal, CheckExternalHealth

router = APIRouter(prefix="/external", tags=["external"])


@router.post("/lookup", response_model=ExternalApiResultResponse)
async def lookup_book(request: BookLookupRequest):
    try:
        use_case = LookupBookExternal()
        result = await use_case.execute(request)
        return ExternalApiResultResponse(
            source=result.source, success=result.success,
            data=result.data, error=result.error,
            latency_ms=result.latency_ms, cached=result.cached,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=ExternalHealthResponse)
async def external_health():
    try:
        use_case = CheckExternalHealth()
        statuses = await use_case.execute()
        overall = "ok" if all(s.status == "ok" for s in statuses) else "degraded"
        return ExternalHealthResponse(
            overall=overall,
            apis=[ApiHealthResponse(
                name=s.name, status=s.status,
                latency_ms=s.latency_ms, last_checked=s.last_checked,
                error=s.error,
            ) for s in statuses]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

main = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.external_router import router

load_dotenv()

app = FastAPI(
    title="External APIs Service",
    description="Capa robusta de integracion con APIs externas para BookFlow - Dev 8 Aldana",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "external-service"}
"""

dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8009
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8009"]
"""

test_entities = """import pytest
from app.domain.entities import ExternalApiResult, ApiHealthStatus
from datetime import datetime


def test_external_api_result_ok():
    result = ExternalApiResult.ok("google_books", {"title": "Clean Code"}, 150.0)
    assert result.success is True
    assert result.source == "google_books"
    assert result.data["title"] == "Clean Code"
    assert result.latency_ms == 150.0
    assert result.cached is False


def test_external_api_result_fail():
    result = ExternalApiResult.fail("google_books", "Timeout", 5000.0)
    assert result.success is False
    assert result.error == "Timeout"
    assert result.data is None


def test_external_api_result_cached():
    result = ExternalApiResult.ok("open_library", {"title": "1984"}, 0, cached=True)
    assert result.cached is True
    assert result.latency_ms == 0


def test_api_health_status():
    status = ApiHealthStatus(
        name="google_books", status="ok",
        latency_ms=120.0, last_checked=datetime.utcnow()
    )
    assert status.name == "google_books"
    assert status.status == "ok"
    assert status.error is None
"""

test_router = """import pytest
from app.routers.external_router import router


def test_router_has_lookup_route():
    routes = [r.path for r in router.routes]
    assert "/external/lookup" in routes


def test_router_has_health_route():
    routes = [r.path for r in router.routes]
    assert "/external/health" in routes


def test_router_prefix():
    assert router.prefix == "/external"
"""

test_clients = """import pytest
from app.infrastructure.google_books_client import GoogleBooksClient
from app.infrastructure.open_library_client import OpenLibraryClient
from app.infrastructure.crossref_client import CrossrefClient


def test_google_books_client_exists():
    client = GoogleBooksClient()
    assert hasattr(client, 'lookup')
    assert hasattr(client, 'health_check')


def test_open_library_client_exists():
    client = OpenLibraryClient()
    assert hasattr(client, 'lookup')
    assert hasattr(client, 'health_check')


def test_crossref_client_exists():
    client = CrossrefClient()
    assert hasattr(client, 'lookup_by_issn')
    assert hasattr(client, 'health_check')
"""

files = {
    'requirements.txt': reqs,
    '.env': env,
    '.env.example': env_example,
    'app/__init__.py': '',
    'app/domain/__init__.py': '',
    'app/application/__init__.py': '',
    'app/infrastructure/__init__.py': '',
    'app/routers/__init__.py': '',
    'tests/__init__.py': '',
    'app/domain/entities.py': entities,
    'app/domain/schemas.py': schemas,
    'app/infrastructure/google_books_client.py': google_books,
    'app/infrastructure/open_library_client.py': open_library,
    'app/infrastructure/crossref_client.py': crossref,
    'app/application/use_cases.py': use_cases,
    'app/routers/external_router.py': router,
    'main.py': main,
    'Dockerfile': dockerfile,
    'tests/test_entities.py': test_entities,
    'tests/test_router.py': test_router,
    'tests/test_clients.py': test_clients,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('External service done!')
