import os
from dotenv import load_dotenv

from app.domain.providers import EnrichmentProvider
from app.infrastructure.providers.mock_provider import MockEnrichmentProvider
from app.infrastructure.providers.google_books_adapter import GoogleBooksAdapter
from app.infrastructure.providers.open_library_adapter import OpenLibraryAdapter
from app.infrastructure.providers.fallback_provider import FallbackProvider
from app.infrastructure.providers.chain_provider import ChainEnrichmentProvider

load_dotenv()


class EnrichmentProviderFactory:
    @staticmethod
    def get_provider() -> EnrichmentProvider:
        provider = os.getenv("ENRICHMENT_PROVIDER", "mock").lower()

        if provider == "mock":
            return MockEnrichmentProvider()

        if provider == "google_books":
            return ChainEnrichmentProvider([
                GoogleBooksAdapter(),
                OpenLibraryAdapter(),
                FallbackProvider(),
            ])

        if provider == "fallback":
            return FallbackProvider()

        raise ValueError(f"Unknown enrichment provider: {provider}")