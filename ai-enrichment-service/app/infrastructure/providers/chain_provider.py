from app.domain.providers import EnrichmentProvider


class ChainEnrichmentProvider(EnrichmentProvider):
    def __init__(self, providers: list[EnrichmentProvider]):
        self.providers = providers

    async def enrich(self, book_reference: str, title: str, author: str, isbn: str):
        last_error = None

        for provider in self.providers:
            try:
                return await provider.enrich(
                    book_reference=book_reference,
                    title=title,
                    author=author,
                    isbn=isbn,
                )
            except Exception as e:
                last_error = e
                continue

        if last_error:
            raise last_error

        raise ValueError("NO_ENRICHMENT_PROVIDER_AVAILABLE")