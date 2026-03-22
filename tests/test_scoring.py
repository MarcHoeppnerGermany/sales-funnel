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
    health = CompanyHealth(
        activity_score=0.8,
        activity_reasoning="Sehr aktiv",
        recent_news=["News 1"],
    )
    affinity = TopicAffinity(
        topic="Cloud",
        affinity_score=0.6,
        affinity_reasoning="Mittel",
    )
    result = score_topic_relevance(health, affinity)
    # 0.8 * 0.4 + 0.6 * 0.6 = 0.32 + 0.36 = 0.68
    assert result.combined_score == 0.68
    assert result.company_health is health
    assert result.topic_affinity is affinity


def test_score_topic_relevance_extremes():
    health = CompanyHealth(activity_score=1.0, activity_reasoning="Max")
    affinity = TopicAffinity(topic="AI", affinity_score=1.0, affinity_reasoning="Max")
    result = score_topic_relevance(health, affinity)
    assert result.combined_score == 1.0

    health_zero = CompanyHealth(activity_score=0.0, activity_reasoning="Min")
    affinity_zero = TopicAffinity(topic="AI", affinity_score=0.0, affinity_reasoning="Min")
    result_zero = score_topic_relevance(health_zero, affinity_zero)
    assert result_zero.combined_score == 0.0


def test_score_customer_rating():
    # hiring=0.15, topic_hiring=0.35, pressure=0.30, size_fit=0.20
    rating = score_customer_rating(0.6, 0.8, 0.7, 0.5)
    expected = round(0.6 * 0.15 + 0.8 * 0.35 + 0.7 * 0.30 + 0.5 * 0.20, 3)
    assert rating == expected


def test_score_customer_rating_zeros():
    rating = score_customer_rating(0.0, 0.0, 0.0, 0.0)
    assert rating == 0.0


def test_score_overall_no_data():
    lead = Lead(company=Company(name="Empty"))
    # No topic_relevance, no financials -> topic_score=0.5, return 0.5*0.5=0.25
    score = score_overall(lead)
    assert score == 0.25


def test_score_overall_with_topic_only():
    lead = Lead(
        company=Company(name="TopicOnly"),
        topic_relevance=TopicRelevance(
            company_health=CompanyHealth(activity_score=0.8, activity_reasoning="Good"),
            topic_affinity=TopicAffinity(topic="AI", affinity_score=0.9, affinity_reasoning="Strong"),
            combined_score=0.86,
        ),
    )
    score = score_overall(lead)
    # topic_score=0.86, no financials -> 0.86 * 0.5 = 0.43
    assert score == 0.43


def test_score_overall_full():
    lead = Lead(
        company=Company(name="Full"),
        topic_relevance=TopicRelevance(
            company_health=CompanyHealth(activity_score=0.7, activity_reasoning="OK"),
            topic_affinity=TopicAffinity(topic="Cloud", affinity_score=0.8, affinity_reasoning="OK"),
            combined_score=0.76,
        ),
        financials=CompanyFinancials(
            hiring_activity=HiringActivity(
                general_hiring_score=0.6, hiring_reasoning="Moderate"
            ),
            topic_hiring=TopicHiring(
                topic_hiring_score=0.9,
                topic_hiring_reasoning="Many relevant",
            ),
            strategic_fit=StrategicFit(
                size_fit_score=0.7,
                financial_health_score=0.5,
                pressure_score=0.8,
                strategic_reasoning="Good fit",
            ),
        ),
    )
    score = score_overall(lead)
    # topic_score=0.76
    # strategic_score = 0.7*0.25 + 0.5*0.25 + 0.8*0.50 = 0.175 + 0.125 + 0.40 = 0.70
    # overall = 0.76*0.25 + 0.70*0.30 + 0.6*0.15 + 0.9*0.30
    #         = 0.19 + 0.21 + 0.09 + 0.27 = 0.76
    assert score == 0.76


def test_rank_leads():
    leads = [
        Lead(company=Company(name="Low")),
        Lead(
            company=Company(name="High"),
            topic_relevance=TopicRelevance(
                company_health=CompanyHealth(activity_score=0.9, activity_reasoning="Great"),
                topic_affinity=TopicAffinity(topic="AI", affinity_score=0.9, affinity_reasoning="Great"),
                combined_score=0.9,
            ),
        ),
    ]
    ranked = rank_leads(leads)
    assert ranked[0].company.name == "High"
    assert ranked[1].company.name == "Low"
    assert ranked[0].overall_score is not None
    assert ranked[1].overall_score is not None
    assert ranked[0].overall_score > ranked[1].overall_score
