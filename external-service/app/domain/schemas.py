from pydantic import BaseModel
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
