import uuid
from datetime import datetime
from app.domain.entities import EnrichmentRequest, EnrichmentStatus
from app.domain.providers import EnrichmentProvider
from app.domain.repositories import EnrichmentRequestRepository, EnrichmentResultRepository
from app.domain.schemas import EnrichBookRequest, EnrichmentResultResponse, EnrichmentRequestResponse


class EnrichBook:

    def __init__(
        self,
        provider: EnrichmentProvider,
        request_repo: EnrichmentRequestRepository,
        result_repo: EnrichmentResultRepository,
    ):
        self.provider = provider
        self.request_repo = request_repo
        self.result_repo = result_repo

    async def execute(self, request: EnrichBookRequest) -> EnrichmentResultResponse:
        enrichment_request = EnrichmentRequest(
            id=uuid.uuid4(),
            book_reference=request.book_reference,
            title=request.title,
            author=request.author,
            isbn=request.isbn,
            status=EnrichmentStatus.PENDING,
            requested_at=datetime.utcnow(),
        )
        saved_request = self.request_repo.save(enrichment_request)

        try:
            result = await self.provider.enrich(
                book_reference=request.book_reference,
                title=request.title or "",
                author=request.author or "",
                isbn=request.isbn or "",
            )
            result.request_id = saved_request.id
            saved_result = self.result_repo.save(result)

            self.request_repo.update_status(
                saved_request.id,
                EnrichmentStatus.COMPLETED.value,
                result.source_used or "fallback_interno"
            )

            return EnrichmentResultResponse(
                id=saved_result.id,
                request_id=saved_result.request_id,
                normalized_title=saved_result.normalized_title,
                normalized_author=saved_result.normalized_author,
                normalized_publisher=saved_result.normalized_publisher,
                normalized_description=saved_result.normalized_description,
                cover_url=saved_result.cover_url,
                metadata_json=saved_result.metadata_json,
            )
        except Exception as e:
            self.request_repo.update_status(
                saved_request.id,
                EnrichmentStatus.FAILED.value,
                None
            )
            raise e


class GetEnrichmentRequest:

    def __init__(self, request_repo: EnrichmentRequestRepository):
        self.request_repo = request_repo

    def execute(self, request_id: uuid.UUID) -> EnrichmentRequestResponse:
        request = self.request_repo.get_by_id(request_id)
        if not request:
            raise ValueError("REQUEST_NOT_FOUND")
        return EnrichmentRequestResponse(
            id=request.id,
            book_reference=request.book_reference,
            status=request.status,
            requested_at=request.requested_at,
            source_used=request.source_used,
        )


class GetEnrichmentRequestsByBookReference:

    def __init__(self, request_repo: EnrichmentRequestRepository):
        self.request_repo = request_repo

    def execute(self, book_reference: str) -> list[EnrichmentRequestResponse]:
        requests = self.request_repo.get_by_book_reference(book_reference)

        return [
            EnrichmentRequestResponse(
                id=request.id,
                book_reference=request.book_reference,
                status=request.status,
                requested_at=request.requested_at,
                source_used=request.source_used,
            )
            for request in requests
        ]