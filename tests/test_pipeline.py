import asyncio

from sales_funnel.agents.base import BaseAgent
from sales_funnel.models.schemas import AgentResult, Company, Lead
from sales_funnel.pipeline import Pipeline


class MockAgent(BaseAgent):
    name = "mock"

    def __init__(self, suffix: str):
        self.suffix = suffix

    async def run(self, input_data=None):
        if isinstance(input_data, AgentResult):
            leads = input_data.leads
        else:
            leads = [Lead(company=Company(name="Initial"))]

        # Jeder Mock-Agent hängt sein Suffix an den Firmennamen
        enriched = []
        for lead in leads:
            updated = lead.model_copy(
                update={
                    "company": lead.company.model_copy(
                        update={"name": f"{lead.company.name}_{self.suffix}"}
                    )
                }
            )
            enriched.append(updated)

        return AgentResult(agent_name=f"mock_{self.suffix}", leads=enriched)


def test_pipeline_chains_agents():
    pipe = Pipeline([MockAgent("A"), MockAgent("B"), MockAgent("C")])
    result = asyncio.run(pipe.run())
    assert len(result.leads) == 1
    assert result.leads[0].company.name == "Initial_A_B_C"


def test_pipeline_with_initial_input():
    initial = AgentResult(
        agent_name="input",
        leads=[
            Lead(company=Company(name="Foo")),
            Lead(company=Company(name="Bar")),
        ],
    )
    pipe = Pipeline([MockAgent("X")])
    result = asyncio.run(pipe.run(initial))
    assert len(result.leads) == 2
    assert result.leads[0].company.name == "Foo_X"


def test_pipeline_describe():
    pipe = Pipeline([MockAgent("A"), MockAgent("B")])
    assert "mock_A" in pipe.describe() or "mock" in pipe.describe()
