from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Company(BaseModel):
    """Stammdaten eines Unternehmens."""

    name: str
    website: str | None = None
    address: str | None = None
    industry: str | None = None
    source: str | None = None


class CompanyHealth(BaseModel):
    """Wie geht es der Firma? Wie aktiv ist sie? (Agent 2, Dimension A)."""

    activity_score: float = Field(ge=0.0, le=1.0)
    activity_reasoning: str
    recent_news: list[str] = []


class TopicAffinity(BaseModel):
    """Wie affin ist die Firma für das vorgegebene Software-Thema? (Agent 2, Dimension B)."""

    topic: str
    affinity_score: float = Field(ge=0.0, le=1.0)
    affinity_reasoning: str
    relevant_news: list[str] = []


class TopicRelevance(BaseModel):
    """Gesamtbewertung aus Agent 2: Firmengesundheit + Themen-Affinität."""

    company_health: CompanyHealth
    topic_affinity: TopicAffinity
    combined_score: float = Field(ge=0.0, le=1.0)


class HiringActivity(BaseModel):
    """Wie aktiv sucht die Firma generell Mitarbeiter? (Agent 3, Dimension A)."""

    general_hiring_score: float = Field(ge=0.0, le=1.0)
    total_job_postings: int | None = None
    hiring_reasoning: str


class TopicHiring(BaseModel):
    """Sucht die Firma Personal, das zum Thema passt? (Agent 3, Dimension B)."""

    topic_hiring_score: float = Field(ge=0.0, le=1.0)
    relevant_job_postings: int | None = None
    topic_hiring_reasoning: str
    example_positions: list[str] = []


class StrategicFit(BaseModel):
    """Strategische Bewertung: Passt die Firma zu uns als Kunde? (Agent 3)."""

    size_fit_score: float = Field(
        ge=0.0, le=1.0,
        description="Passt die Größenordnung der Firma zu uns?",
    )
    financial_health_score: float = Field(
        ge=0.0, le=1.0,
        description="Wie gut ist die Firma finanziell aufgestellt?",
    )
    pressure_score: float = Field(
        ge=0.0, le=1.0,
        description="Hat die Firma Druck im Thema? (auch schlecht situierte Firmen mit Handlungsdruck sind interessant)",
    )
    strategic_reasoning: str = Field(
        description="Begründung der strategischen Bewertung. Berücksichtige: "
        "Firmen denen es schlecht geht, die aber dadurch Druck im Thema haben, "
        "können sehr interessante Kunden sein.",
    )


class CompanyFinancials(BaseModel):
    """Finanzkennzahlen und Kundenbewertung (Agent 3)."""

    revenue_estimate: str | None = None
    profit_estimate: str | None = None
    employee_count: int | None = None
    hiring_activity: HiringActivity | None = None
    topic_hiring: TopicHiring | None = None
    strategic_fit: StrategicFit | None = None
    customer_rating: float = Field(ge=0.0, le=1.0, default=0.0)
    rating_reasoning: str = ""


class Lead(BaseModel):
    """Akkumulator-Objekt: wird von jedem Agenten angereichert."""

    company: Company
    topic_relevance: TopicRelevance | None = None
    financials: CompanyFinancials | None = None
    overall_score: float | None = None


class AgentResult(BaseModel):
    """Standard-Rückgabe jedes Agenten."""

    agent_name: str
    leads: list[Lead]
    metadata: dict = {}
    timestamp: datetime = Field(default_factory=datetime.now)
