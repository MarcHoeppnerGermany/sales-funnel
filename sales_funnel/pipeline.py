from __future__ import annotations

from sales_funnel.agents.base import BaseAgent
from sales_funnel.models.schemas import AgentResult


class Pipeline:
    """Orchestriert Agenten sequenziell. Output von Agent N wird Input von Agent N+1."""

    def __init__(self, agents: list[BaseAgent]):
        self.agents = agents

    async def run(self, initial_input: dict | AgentResult | None = None) -> AgentResult:
        result: dict | AgentResult | None = initial_input

        for agent in self.agents:
            result = await agent.run(result)

        if not isinstance(result, AgentResult):
            raise RuntimeError("Pipeline hat kein AgentResult produziert")

        return result

    def describe(self) -> str:
        names = " → ".join(a.name for a in self.agents)
        return f"Pipeline: {names}"
