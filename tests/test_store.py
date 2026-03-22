import json

import pytest

from sales_funnel.models.schemas import (
    Company,
    CompanyFinancials,
    CompanyHealth,
    Lead,
    TopicAffinity,
    TopicRelevance,
)
from sales_funnel.store import LeadStore


@pytest.fixture
def tmp_store(tmp_path):
    """Create a LeadStore with a temporary file."""
    path = str(tmp_path / "test_leads.json")
    return LeadStore(path=path)


def _make_lead(name: str, **kwargs) -> Lead:
    return Lead(company=Company(name=name, **kwargs))


class TestLeadStoreLoad:
    def test_load_empty(self, tmp_store):
        result = tmp_store.load()
        assert result.leads == []
        assert result.agent_name == "store"

    def test_load_existing(self, tmp_store):
        lead = _make_lead("Test GmbH", website="https://test.de")
        tmp_store.add_leads([lead])
        result = tmp_store.load()
        assert len(result.leads) == 1
        assert result.leads[0].company.name == "Test GmbH"


class TestLeadStoreAdd:
    def test_add_single(self, tmp_store):
        lead = _make_lead("Acme Corp")
        result = tmp_store.add_leads([lead])
        assert len(result.leads) == 1

    def test_add_multiple(self, tmp_store):
        leads = [_make_lead("A"), _make_lead("B"), _make_lead("C")]
        result = tmp_store.add_leads(leads)
        assert len(result.leads) == 3

    def test_add_deduplicates(self, tmp_store):
        tmp_store.add_leads([_make_lead("Acme")])
        result = tmp_store.add_leads([_make_lead("Acme")])
        assert len(result.leads) == 1

    def test_add_deduplicates_case_insensitive(self, tmp_store):
        tmp_store.add_leads([_make_lead("Acme Corp")])
        result = tmp_store.add_leads([_make_lead("acme corp")])
        assert len(result.leads) == 1

    def test_add_persists(self, tmp_store):
        tmp_store.add_leads([_make_lead("Persistent")])
        store2 = LeadStore(path=str(tmp_store.path))
        result = store2.load()
        assert len(result.leads) == 1
        assert result.leads[0].company.name == "Persistent"


class TestLeadStoreUpdate:
    def test_update_lead(self, tmp_store):
        tmp_store.add_leads([_make_lead("Test")])
        topic_relevance = TopicRelevance(
            company_health=CompanyHealth(
                activity_score=0.8, activity_reasoning="Good"
            ),
            topic_affinity=TopicAffinity(
                topic="AI", affinity_score=0.9, affinity_reasoning="Strong"
            ),
            combined_score=0.86,
        )
        updated = tmp_store.update_lead("Test", topic_relevance=topic_relevance)
        assert updated.topic_relevance is not None
        assert updated.topic_relevance.combined_score == 0.86

    def test_update_nonexistent_raises(self, tmp_store):
        with pytest.raises(KeyError):
            tmp_store.update_lead("Nonexistent", overall_score=0.5)

    def test_update_case_insensitive(self, tmp_store):
        tmp_store.add_leads([_make_lead("Test Corp")])
        updated = tmp_store.update_lead("test corp", overall_score=0.7)
        assert updated.overall_score == 0.7


class TestLeadStoreGet:
    def test_get_existing(self, tmp_store):
        tmp_store.add_leads([_make_lead("Find Me")])
        lead = tmp_store.get_lead("Find Me")
        assert lead is not None
        assert lead.company.name == "Find Me"

    def test_get_nonexistent(self, tmp_store):
        assert tmp_store.get_lead("Ghost") is None

    def test_get_case_insensitive(self, tmp_store):
        tmp_store.add_leads([_make_lead("CamelCase")])
        lead = tmp_store.get_lead("camelcase")
        assert lead is not None


class TestLeadStoreRemove:
    def test_remove_existing(self, tmp_store):
        tmp_store.add_leads([_make_lead("Gone")])
        assert tmp_store.remove_lead("Gone") is True
        assert tmp_store.get_lead("Gone") is None

    def test_remove_nonexistent(self, tmp_store):
        assert tmp_store.remove_lead("Nope") is False

    def test_remove_case_insensitive(self, tmp_store):
        tmp_store.add_leads([_make_lead("Remove Me")])
        assert tmp_store.remove_lead("remove me") is True
        assert len(tmp_store.load().leads) == 0
