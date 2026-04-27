content = open('ai-enrichment-service/app/application/use_cases.py', 'r', encoding='utf-8').read()
content = content.replace(
    'self.request_repo.update_status(saved_request.id, EnrichmentStatus.COMPLETED.value, "mock")',
    'source = getattr(result, "source_used", None) or getattr(result.metadata_json, "__getitem__", lambda x: "google_books")("source") if isinstance(result.metadata_json, dict) else "google_books"\n            self.request_repo.update_status(saved_request.id, EnrichmentStatus.COMPLETED.value, source)'
)
with open('ai-enrichment-service/app/application/use_cases.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
