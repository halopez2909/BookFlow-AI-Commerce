content = """DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/enrichment_db
ENRICHMENT_PROVIDER=google_books
ENRICHMENT_TIMEOUT_SECONDS=10
MOCK_LATENCY_MS=500
"""
with open('ai-enrichment-service/.env', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
