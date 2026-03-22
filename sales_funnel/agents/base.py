from __future__ import annotations

from abc import ABC, abstractmethod

from sales_funnel.models.schemas import AgentResult


class BaseAgent(ABC):
    """Basisklasse für alle Agenten."""

    name: str

    @abstractmethod
    async def run(self, input_data: AgentResult | dict | None = None) -> AgentResult:
        ...
