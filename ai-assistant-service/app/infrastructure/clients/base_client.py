"""
Cliente HTTP base. Centraliza el AsyncClient de httpx, el timeout
configurable por env y el manejo de errores: NUNCA lanza excepción
al caller; en caso de fallo devuelve None y loggea.
"""
import logging
import os
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)


class BaseHttpClient:
    def __init__(self, base_url: str, timeout: float | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout if timeout is not None else float(
            os.getenv("HTTP_TIMEOUT", "5")
        )

    async def _get(self, path: str, params: dict | None = None) -> Optional[Any]:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            logger.warning("HTTP %s en %s: %s", exc.response.status_code, url, exc)
            return None
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            logger.warning("Fallo de red en %s: %s", url, exc)
            return None
        except Exception as exc:
            logger.exception("Error inesperado consultando %s: %s", url, exc)
            return None