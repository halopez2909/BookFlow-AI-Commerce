import os
from dotenv import load_dotenv
from app.domain.providers import EnrichmentProvider
from app.infrastructure.providers.mock_provider import MockEnrichmentProvider
from app.infrastructure.providers.google_books_adapter import GoogleBooksAdapter

load_dotenv()


class EnrichmentProviderFactory:

    @staticmethod
    def get_provider() -> EnrichmentProvider:
        provider = os.getenv("ENRICHMENT_PROVIDER", "mock").lower()
        if provider == "mock":
            return MockEnrichmentProvider()
        elif provider == "google_books":
            return GoogleBooksAdapter()
        raise ValueError(f"Unknown enrichment provider: {provider}")
