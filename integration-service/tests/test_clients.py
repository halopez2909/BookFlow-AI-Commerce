import pytest
from app.infrastructure.clients import (
    InventoryClient, EnrichmentClient,
    NormalizationClient, CatalogClient
)


def test_inventory_client_exists():
    client = InventoryClient()
    assert hasattr(client, 'get_batch')
    assert hasattr(client, 'get_batch_items')


def test_enrichment_client_exists():
    client = EnrichmentClient()
    assert hasattr(client, 'enrich')


def test_normalization_client_exists():
    client = NormalizationClient()
    assert hasattr(client, 'normalize')


def test_catalog_client_exists():
    client = CatalogClient()
    assert hasattr(client, 'get_categories')
    assert hasattr(client, 'register_book')
