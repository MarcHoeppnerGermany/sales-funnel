import json
import tempfile
from pathlib import Path

from sales_funnel.models.schemas import AgentResult, Company, Lead
from sales_funnel.store import LeadStore


def _tmp_store() -> tuple[LeadStore, Path]:
    f = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    f.close()
    path = Path(f.name)
    path.unlink()  # start fresh
    return LeadStore(path=str(path)), path


def test_store_create_and_load():
    store, path = _tmp_store()
    try:
        result = store.load()
        assert result.leads == []

        store.add_leads([Lead(company=Company(name="Acme"))])
        result = store.load()
        assert len(result.leads) == 1
        assert result.leads[0].company.name == "Acme"
    finally:
        path.unlink(missing_ok=True)


def test_store_deduplication():
    store, path = _tmp_store()
    try:
        store.add_leads([
            Lead(company=Company(name="Acme")),
            Lead(company=Company(name="acme")),  # same, different case
            Lead(company=Company(name="Beta")),
        ])
        result = store.load()
        assert len(result.leads) == 2
    finally:
        path.unlink(missing_ok=True)


def test_store_update_lead():
    store, path = _tmp_store()
    try:
        store.add_leads([Lead(company=Company(name="Acme"))])
        updated = store.update_lead("Acme", overall_score=0.75)
        assert updated.overall_score == 0.75

        reloaded = store.get_lead("Acme")
        assert reloaded.overall_score == 0.75
    finally:
        path.unlink(missing_ok=True)


def test_store_remove_lead():
    store, path = _tmp_store()
    try:
        store.add_leads([
            Lead(company=Company(name="Acme")),
            Lead(company=Company(name="Beta")),
        ])
        assert store.remove_lead("Acme") is True
        assert store.remove_lead("Acme") is False
        assert len(store.load().leads) == 1
    finally:
        path.unlink(missing_ok=True)


def test_store_get_lead_case_insensitive():
    store, path = _tmp_store()
    try:
        store.add_leads([Lead(company=Company(name="Acme Corp"))])
        assert store.get_lead("acme corp") is not None
        assert store.get_lead("ACME CORP") is not None
        assert store.get_lead("unknown") is None
    finally:
        path.unlink(missing_ok=True)
