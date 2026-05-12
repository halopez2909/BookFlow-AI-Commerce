import os
from app.domain.providers import EnrichmentProvider
from app.infrastructure.providers.mock_provider import MockEnrichmentProvider
from app.infrastructure.providers.google_books_adapter import GoogleBooksAdapter
from app.infrastructure.providers.open_library_adapter import OpenLibraryAdapter
from app.infrastructure.providers.fallback_provider import FallbackProvider
from dotenv import load_dotenv

load_dotenv()


class ChainedEnrichmentProvider(EnrichmentProvider):
    def __init__(self, providers):
        self.providers = providers

    async def enrich(self, book_reference, title, author, isbn=None):
        for provider in self.providers:
            try:
                result = await provider.enrich(book_reference, title, author, isbn)
                if result:
                    return result
            except Exception:
                continue
        return await FallbackProvider().enrich(book_reference, title, author, isbn)


class EnrichmentProviderFactory:
    @staticmethod
    def get_provider() -> EnrichmentProvider:
        provider = os.getenv("ENRICHMENT_PROVIDER", "mock")
        if provider == "google_books":
            return ChainedEnrichmentProvider([
                GoogleBooksAdapter(),
                OpenLibraryAdapter(),
                FallbackProvider(),
            ])
        return MockEnrichmentProvider()
