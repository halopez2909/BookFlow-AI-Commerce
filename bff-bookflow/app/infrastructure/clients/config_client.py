SYSTEM_PARAMS = {
    "INVENTORY_MAX_FILE_SIZE_MB": "10",
    "ENRICHMENT_PROVIDER": "mock",
    "MOCK_LATENCY_MS": "500",
}


class ConfigClient:

    def get_params(self) -> dict:
        return SYSTEM_PARAMS

    def update_params(self, params: dict) -> dict:
        SYSTEM_PARAMS.update(params)
        return SYSTEM_PARAMS
