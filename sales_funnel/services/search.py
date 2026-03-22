from __future__ import annotations

import asyncio
import os

import httpx
from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class SearchService:
    """Web-Suche über Brave Search API."""

    def __init__(self, api_key: str | None = None, max_concurrent: int = 5):
        self.api_key = api_key or os.environ.get("BRAVE_API_KEY", "")
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def search(self, query: str, num_results: int = 10) -> list[SearchResult]:
        if not self.api_key:
            return self._mock_search(query, num_results)

        async with self._semaphore:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    headers={
                        "X-Subscription-Token": self.api_key,
                        "Accept": "application/json",
                    },
                    params={"q": query, "count": num_results},
                )
                resp.raise_for_status()
                data = resp.json()

            results = []
            for item in data.get("web", {}).get("results", [])[:num_results]:
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        snippet=item.get("description", ""),
                    )
                )
            return results

    def _mock_search(self, query: str, num_results: int) -> list[SearchResult]:
        """Fallback wenn kein API-Key gesetzt ist – gibt leere Ergebnisse zurück."""
        return []
