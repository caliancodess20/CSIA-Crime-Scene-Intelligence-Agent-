# backend/app/timeline_suggestions/test_full_flow.py

"""
End-to-end API test for the Timeline & Next-Step Suggestions routes,
using FastAPI's TestClient. Replaces the old Flask test_full_flow.py
(which hit POST /timeline/suggestions on a standalone Flask app).

This test overrides two real dependencies so it doesn't need a live
database or a real login:
  - get_db            (from app.case_management.database)
  - get_current_user   (from app.shared.auth)

Run with:
    pytest backend/app/timeline_suggestions/test_full_flow.py -v

NOTE: This assumes `app.main.app` is the shared FastAPI instance with
both case_management and timeline_suggestions routers registered (see
main.py). If your test runner can't import `app.main` yet because
case_management's imports aren't fully wired up, run test_timeline.py
and test_next_steps.py first — those don't need the full app.
"""

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.case_management.database import get_db
from app.shared.auth import get_current_user


class FakeEvidence(SimpleNamespace):
    """Mimics enough of the real SQLAlchemy Evidence model for these tests."""
    pass


class FakeCase(SimpleNamespace):
    """Mimics enough of the real SQLAlchemy Case model for these tests."""
    pass


def _build_fake_case(with_evidence: bool = True) -> FakeCase:
    evidence_items = []
    if with_evidence:
        evidence_items = [
            FakeEvidence(
                id=uuid.uuid4(),
                case_id=uuid.uuid4(),
                evidence_type="image",
                description=None,
                source="Test camera",
                collected_by="Test Officer",
                collected_at=datetime(2026, 8, 24, 11, 0, tzinfo=timezone.utc),
                extra_metadata={"yolo_detections": ["knife"]},
            ),
            FakeEvidence(
                id=uuid.uuid4(),
                case_id=uuid.uuid4(),
                evidence_type="witness_statement",
                description="Shopkeeper statement",
                source="Shopkeeper",
                collected_by="Insp. Test",
                collected_at=datetime(2026, 8, 24, 14, 0, tzinfo=timezone.utc),
                extra_metadata={"nlp_entities": {"names": ["Test Witness"]}},
            ),
        ]
    return FakeCase(id=uuid.uuid4(), evidence_items=evidence_items)


@pytest.fixture
def client(monkeypatch):
    # Fake DB session — routes only ever pass this through to crud.get_case,
    # so we patch crud.get_case directly instead of building a real Session.
    def fake_get_db():
        yield None

    def fake_get_current_user():
        return {"id": "test-user", "role": "investigator"}

    app.dependency_overrides[get_db] = fake_get_db
    app.dependency_overrides[get_current_user] = fake_get_current_user

    yield TestClient(app)

    app.dependency_overrides.clear()


class TestTimelineEndpoint:

    def test_get_timeline_returns_ordered_events(self, client, monkeypatch):
        fake_case = _build_fake_case(with_evidence=True)

        import app.timeline_suggestions.routes as routes_module
        monkeypatch.setattr(routes_module.crud, "get_case", lambda db, case_id: fake_case)

        response = client.get(f"/cases/{fake_case.id}/timeline")

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert len(body["timeline"]) == 2
        assert body["timeline"][0]["event"] != body["timeline"][1]["event"]

    def test_get_timeline_case_not_found_returns_404(self, client, monkeypatch):
        import app.timeline_suggestions.routes as routes_module
        monkeypatch.setattr(routes_module.crud, "get_case", lambda db, case_id: None)

        response = client.get(f"/cases/{uuid.uuid4()}/timeline")

        assert response.status_code == 404

    def test_get_timeline_no_evidence_returns_422(self, client, monkeypatch):
        fake_case = _build_fake_case(with_evidence=False)

        import app.timeline_suggestions.routes as routes_module
        monkeypatch.setattr(routes_module.crud, "get_case", lambda db, case_id: fake_case)

        response = client.get(f"/cases/{fake_case.id}/timeline")

        assert response.status_code == 422


class TestNextStepsEndpoint:

    def test_get_next_steps_returns_suggestions(self, client, monkeypatch):
        fake_case = _build_fake_case(with_evidence=True)

        import app.timeline_suggestions.routes as routes_module
        monkeypatch.setattr(routes_module.crud, "get_case", lambda db, case_id: fake_case)

        response = client.get(f"/cases/{fake_case.id}/next-steps")

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["next_steps"], list)
        assert len(body["next_steps"]) > 0


class TestCombinedEndpoint:

    def test_get_timeline_and_next_steps_together(self, client, monkeypatch):
        fake_case = _build_fake_case(with_evidence=True)

        import app.timeline_suggestions.routes as routes_module
        monkeypatch.setattr(routes_module.crud, "get_case", lambda db, case_id: fake_case)

        response = client.get(f"/cases/{fake_case.id}/timeline-and-next-steps")

        assert response.status_code == 200
        body = response.json()
        assert "timeline" in body
        assert "next_steps" in body
