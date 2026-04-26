import os
from typing import List
from app.domain.entities import IntegrationFlow, FlowStatus
from app.domain.repositories import IntegrationFlowRepository
from app.infrastructure.clients import (
    InventoryClient, EnrichmentClient, NormalizationClient, CatalogClient
)


class TriggerEnrichmentFlow:
    def __init__(self, repository: IntegrationFlowRepository):
        self.repository = repository
        self.inventory_client = InventoryClient()
        self.enrichment_client = EnrichmentClient()
        self.normalization_client = NormalizationClient()
        self.catalog_client = CatalogClient()

    async def execute(self, batch_id: str) -> IntegrationFlow:
        flow = IntegrationFlow.create(batch_id)
        flow.status = FlowStatus.RUNNING
        self.repository.save(flow)

        # Step 1: Inventory
        inventory_step = flow.get_step("inventory")
        inventory_step.start()
        try:
            batch = await self.inventory_client.get_batch(batch_id)
            flow.total_books = batch.get("valid_rows", 0)
            inventory_step.complete()
        except Exception as e:
            inventory_step.fail(str(e))
            flow.update_status()
            self.repository.save(flow)
            return flow
        self.repository.save(flow)

        # Step 2: Enrichment
        enrichment_step = flow.get_step("enrichment")
        enrichment_step.start()
        enriched_results = []
        try:
            books = [
                {"book_reference": f"REF-{batch_id}-{i}", "title": f"Book {i}", "author": "Unknown"}
                for i in range(min(flow.total_books, 5))
            ]
            for book in books:
                try:
                    result = await self.enrichment_client.enrich(
                        book_reference=book["book_reference"],
                        title=book["title"],
                        author=book["author"],
                    )
                    enriched_results.append(result)
                    flow.processed_books += 1
                except Exception:
                    flow.failed_books += 1
            enrichment_step.complete()
        except Exception as e:
            enrichment_step.fail(str(e))
        self.repository.save(flow)

        # Step 3: Normalization
        normalization_step = flow.get_step("normalization")
        normalization_step.start()
        normalized_results = []
        try:
            for result in enriched_results:
                try:
                    normalized = await self.normalization_client.normalize(
                        enrichment_result_id=result.get("id", "unknown"),
                        title=result.get("normalized_title", "Unknown"),
                        author=result.get("normalized_author", "Unknown"),
                        isbn=result.get("normalized_isbn"),
                    )
                    normalized_results.append(normalized)
                except Exception:
                    pass
            normalization_step.complete()
        except Exception as e:
            normalization_step.fail(str(e))
        self.repository.save(flow)

        # Step 4: Catalog
        catalog_step = flow.get_step("catalog")
        catalog_step.start()
        try:
            categories = await self.catalog_client.get_categories()
            default_category_id = categories[0]["id"] if categories else None
            for normalized in normalized_results:
                try:
                    if default_category_id and not normalized.get("is_duplicate"):
                        await self.catalog_client.register_book({
                            "title": normalized.get("normalized_title", "Unknown"),
                            "author": normalized.get("normalized_author", "Unknown"),
                            "publisher": "BookFlow Import",
                            "category_id": default_category_id,
                            "isbn": normalized.get("normalized_isbn"),
                        })
                except Exception:
                    pass
            catalog_step.complete()
        except Exception as e:
            catalog_step.fail(str(e))
        self.repository.save(flow)

        flow.update_status()
        self.repository.save(flow)
        return flow


class GetFlowStatus:
    def __init__(self, repository: IntegrationFlowRepository):
        self.repository = repository

    def execute(self, batch_id: str):
        return self.repository.find_by_batch_id(batch_id)


class GetAllFlows:
    def __init__(self, repository: IntegrationFlowRepository):
        self.repository = repository

    def execute(self):
        return self.repository.find_all()
