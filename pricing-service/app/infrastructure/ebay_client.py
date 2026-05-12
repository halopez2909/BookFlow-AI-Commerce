import os
import httpx
from typing import Optional
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID", "")
TIMEOUT = int(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", "10"))

_cache = TTLCache(maxsize=256, ttl=3600)


class EbayPriceClient:
    async def get_reference_price(self, isbn: Optional[str], title: Optional[str]) -> Optional[float]:
        if not EBAY_APP_ID or not isbn:
            return None
        cache_key = f"ebay:{isbn}"
        if cache_key in _cache:
            return _cache[cache_key]
        try:
            price = await self._fetch_ebay(isbn, title)
            if price:
                _cache[cache_key] = price
            return price
        except Exception:
            return None

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=False,
    )
    async def _fetch_ebay(self, isbn: str, title: Optional[str]) -> Optional[float]:
        query = isbn or title or ""
        url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        headers = {"Authorization": f"Bearer {EBAY_APP_ID}"}
        params = {"q": f"book {query}", "limit": 5, "category_ids": "267"}
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(url, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
            items = data.get("itemSummaries", [])
            if not items:
                return None
            prices = []
            for item in items:
                try:
                    p = float(item["price"]["value"])
                    prices.append(p * 4200)
                except Exception:
                    continue
            return round(sum(prices) / len(prices), -2) if prices else None
