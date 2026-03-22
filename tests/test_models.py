from sales_funnel.models.schemas import (
    AgentResult,
    Company,
    CompanyFinancials,
    CompanyHealth,
    HiringActivity,
    Lead,
    StrategicFit,
    TopicAffinity,
    TopicHiring,
    TopicRelevance,
)


def test_company_creation():
    c = Company(name="Test GmbH", website="https://test.de")
    assert c.name == "Test GmbH"
    assert c.address is None


def test_lead_accumulation():
    lead = Lead(company=Company(name="Acme"))
    assert lead.topic_relevance is None
    assert lead.financials is None

    # Agent 2 enrichment
    lead = lead.model_copy(
        update={
            "topic_relevance": TopicRelevance(
                company_health=CompanyHealth(
                    activity_score=0.7,
                    activity_reasoning="Aktiv in Nachrichten",
                    recent_news=["Acme expandiert"],
                ),
                topic_affinity=TopicAffinity(
                    topic="Cloud",
                    affinity_score=0.8,
                    affinity_reasoning="Starke Cloud-Initiativen",
                ),
                combined_score=0.76,
            )
        }
    )
    assert lead.topic_relevance is not None
    assert lead.topic_relevance.combined_score == 0.76

    # Agent 3 enrichment
    lead = lead.model_copy(
        update={
            "financials": CompanyFinancials(
                revenue_estimate="10M",
                employee_count=50,
                hiring_activity=HiringActivity(
                    general_hiring_score=0.6,
                    total_job_postings=12,
                    hiring_reasoning="Moderates Wachstum",
                ),
                topic_hiring=TopicHiring(
                    topic_hiring_score=0.8,
                    relevant_job_postings=3,
                    topic_hiring_reasoning="Sucht Cloud Engineers",
                    example_positions=["Cloud Engineer", "DevOps"],
                ),
                strategic_fit=StrategicFit(
                    size_fit_score=0.7,
                    financial_health_score=0.6,
                    pressure_score=0.9,
                    strategic_reasoning="Unter Modernisierungsdruck",
                ),
                customer_rating=0.75,
                rating_reasoning="Guter Fit",
            )
        }
    )
    assert lead.financials is not None
    assert lead.financials.strategic_fit.pressure_score == 0.9


def test_agent_result_serialization():
    result = AgentResult(
        agent_name="test",
        leads=[Lead(company=Company(name="Foo"))],
        metadata={"key": "val"},
    )
    json_str = result.model_dump_json()
    restored = AgentResult.model_validate_json(json_str)
    assert restored.leads[0].company.name == "Foo"
    assert restored.metadata["key"] == "val"


def test_lead_full_roundtrip():
    lead = Lead(
        company=Company(name="Bar", website="https://bar.de", industry="IT"),
        topic_relevance=TopicRelevance(
            company_health=CompanyHealth(
                activity_score=0.5,
                activity_reasoning="Mittelmäßig",
            ),
            topic_affinity=TopicAffinity(
                topic="AI",
                affinity_score=0.9,
                affinity_reasoning="Stark in AI",
            ),
            combined_score=0.74,
        ),
        financials=CompanyFinancials(
            customer_rating=0.85,
            rating_reasoning="Great",
            strategic_fit=StrategicFit(
                size_fit_score=0.8,
                financial_health_score=0.3,
                pressure_score=0.95,
                strategic_reasoning="Schlecht situiert aber hoher Druck = interessant",
            ),
        ),
        overall_score=0.87,
    )
    data = lead.model_dump_json()
    restored = Lead.model_validate_json(data)
    assert restored.overall_score == 0.87
    assert restored.financials.strategic_fit.pressure_score == 0.95
    assert restored.topic_relevance.topic_affinity.topic == "AI"
