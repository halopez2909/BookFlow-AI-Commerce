from fastapi import APIRouter, HTTPException
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
