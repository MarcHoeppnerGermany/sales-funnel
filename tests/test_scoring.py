from sales_funnel.models.schemas import (
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
from sales_funnel.scoring import (
    rank_leads,
    score_customer_rating,
    score_overall,
    score_topic_relevance,
)


def test_score_topic_relevance():
    health = CompanyHealth(activity_score=0.8, activity_reasoning="Aktiv")
    affinity = TopicAffinity(topic="Cloud", affinity_score=0.6, affinity_reasoning="OK")
    result = score_topic_relevance(health, affinity)
    # 0.8 * 0.4 + 0.6 * 0.6 = 0.32 + 0.36 = 0.68
    assert result.combined_score == 0.68


def test_score_customer_rating():
    rating = score_customer_rating(
        hiring_score=0.5,
        topic_hiring_score=0.8,
        pressure_score=0.9,
        size_fit_score=0.7,
    )
    # 0.5*0.15 + 0.8*0.35 + 0.9*0.30 + 0.7*0.20 = 0.075 + 0.28 + 0.27 + 0.14 = 0.765
    assert rating == 0.765


def test_score_overall_full_data():
    lead = Lead(
        company=Company(name="Test"),
        topic_relevance=TopicRelevance(
            company_health=CompanyHealth(activity_score=0.7, activity_reasoning="OK"),
            topic_affinity=TopicAffinity(topic="AI", affinity_score=0.9, affinity_reasoning="Gut"),
            combined_score=0.82,
        ),
        financials=CompanyFinancials(
            hiring_activity=HiringActivity(
                general_hiring_score=0.6, hiring_reasoning="Moderate"
            ),
            topic_hiring=TopicHiring(
                topic_hiring_score=0.8, topic_hiring_reasoning="Sucht AI Experten"
            ),
            strategic_fit=StrategicFit(
                size_fit_score=0.7,
                financial_health_score=0.5,
                pressure_score=0.9,
                strategic_reasoning="Hoher Druck",
            ),
        ),
    )
    score = score_overall(lead)
    # topic: 0.82*0.25 = 0.205
    # strategic: (0.7*0.25 + 0.5*0.25 + 0.9*0.50) = 0.175+0.125+0.45 = 0.75 -> 0.75*0.30 = 0.225
    # hiring: 0.6*0.15 = 0.09
    # topic_hiring: 0.8*0.30 = 0.24
    # total = 0.205 + 0.225 + 0.09 + 0.24 = 0.76
    assert score == 0.76


def test_score_overall_no_financials():
    lead = Lead(
        company=Company(name="Test"),
        topic_relevance=TopicRelevance(
            company_health=CompanyHealth(activity_score=0.6, activity_reasoning="OK"),
            topic_affinity=TopicAffinity(topic="AI", affinity_score=0.8, affinity_reasoning="Gut"),
            combined_score=0.72,
        ),
    )
    score = score_overall(lead)
    # 0.72 * 0.5 = 0.36
    assert score == 0.36


def test_score_overall_empty_lead():
    lead = Lead(company=Company(name="Empty"))
    score = score_overall(lead)
    # default topic_score = 0.5, no financials -> 0.5 * 0.5 = 0.25
    assert score == 0.25


def test_rank_leads():
    leads = [
        Lead(company=Company(name="Low")),
        Lead(
            company=Company(name="High"),
            topic_relevance=TopicRelevance(
                company_health=CompanyHealth(activity_score=0.9, activity_reasoning="Gut"),
                topic_affinity=TopicAffinity(topic="X", affinity_score=0.9, affinity_reasoning="Stark"),
                combined_score=0.9,
            ),
            financials=CompanyFinancials(
                hiring_activity=HiringActivity(general_hiring_score=0.9, hiring_reasoning="Viel"),
                topic_hiring=TopicHiring(topic_hiring_score=0.9, topic_hiring_reasoning="Stark"),
                strategic_fit=StrategicFit(
                    size_fit_score=0.9,
                    financial_health_score=0.9,
                    pressure_score=0.9,
                    strategic_reasoning="Perfekt",
                ),
            ),
        ),
    ]
    ranked = rank_leads(leads)
    assert ranked[0].company.name == "High"
    assert ranked[1].company.name == "Low"
    assert ranked[0].overall_score > ranked[1].overall_score
