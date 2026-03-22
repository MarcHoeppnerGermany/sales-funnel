from __future__ import annotations

from sales_funnel.models.schemas import (
    CompanyHealth,
    Lead,
    TopicAffinity,
    TopicRelevance,
)


def score_topic_relevance(
    health: CompanyHealth, affinity: TopicAffinity
) -> TopicRelevance:
    """Berechnet combined_score aus health + affinity."""
    combined = health.activity_score * 0.4 + affinity.affinity_score * 0.6
    return TopicRelevance(
        company_health=health,
        topic_affinity=affinity,
        combined_score=round(combined, 3),
    )


def score_customer_rating(
    hiring_score: float,
    topic_hiring_score: float,
    pressure_score: float,
    size_fit_score: float,
) -> float:
    """Berechnet customer_rating."""
    return round(
        hiring_score * 0.15
        + topic_hiring_score * 0.35
        + pressure_score * 0.30
        + size_fit_score * 0.20,
        3,
    )


def score_overall(lead: Lead) -> float:
    """Berechnet overall_score aus allen Dimensionen."""
    topic_score = (
        lead.topic_relevance.combined_score if lead.topic_relevance else 0.5
    )
    fin = lead.financials
    if fin:
        hiring_score = (
            fin.hiring_activity.general_hiring_score
            if fin.hiring_activity
            else 0.0
        )
        topic_hiring_score = (
            fin.topic_hiring.topic_hiring_score if fin.topic_hiring else 0.0
        )
        strategic = fin.strategic_fit
        if strategic:
            strategic_score = (
                strategic.size_fit_score * 0.25
                + strategic.financial_health_score * 0.25
                + strategic.pressure_score * 0.50
            )
        else:
            strategic_score = 0.5
        return round(
            topic_score * 0.25
            + strategic_score * 0.30
            + hiring_score * 0.15
            + topic_hiring_score * 0.30,
            3,
        )
    return round(topic_score * 0.5, 3)


def rank_leads(leads: list[Lead]) -> list[Lead]:
    """Sortiert Leads nach overall_score absteigend."""
    for lead in leads:
        lead.overall_score = score_overall(lead)
    return sorted(leads, key=lambda l: l.overall_score or 0, reverse=True)
