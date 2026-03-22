from __future__ import annotations

import json
import os
from typing import TypeVar

import anthropic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMService:
    """Wrapper für die Anthropic Claude API mit strukturierter Ausgabe."""

    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get(
            "ANTHROPIC_MODEL", "claude-sonnet-4-20250514"
        )
        self.client = anthropic.AsyncAnthropic()
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    async def structured_query(
        self,
        system: str,
        prompt: str,
        response_model: type[T],
    ) -> T:
        """Sendet Prompt an Claude und parst Antwort in ein Pydantic-Modell."""
        schema = response_model.model_json_schema()

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            tools=[
                {
                    "name": "output",
                    "description": "Structured output",
                    "input_schema": schema,
                }
            ],
            tool_choice={"type": "tool", "name": "output"},
        )

        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        for block in response.content:
            if block.type == "tool_use" and block.name == "output":
                return response_model.model_validate(block.input)

        raise ValueError("Keine strukturierte Antwort von Claude erhalten")

    async def text_query(self, system: str, prompt: str) -> str:
        """Einfache Textantwort von Claude."""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )

        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        return response.content[0].text

    async def generate_search_queries(self, criteria: dict) -> list[str]:
        """Generiert optimale Suchbegriffe aus den Suchkriterien."""
        prompt = (
            "Generiere 3-5 verschiedene Web-Suchbegriffe, um Unternehmen zu finden, "
            "die zu folgenden Kriterien passen. Gib NUR die Suchbegriffe zurück, "
            "einen pro Zeile, ohne Nummerierung.\n\n"
            f"Kriterien: {json.dumps(criteria, ensure_ascii=False)}"
        )

        text = await self.text_query(
            system="Du bist ein Experte für B2B-Recherche und Leadgenerierung.",
            prompt=prompt,
        )

        return [line.strip() for line in text.strip().splitlines() if line.strip()]
