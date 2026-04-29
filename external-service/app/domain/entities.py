from dataclasses import dataclass
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
