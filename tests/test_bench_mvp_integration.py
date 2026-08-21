from datetime import datetime, timezone

import pytest

from hoofcare.integration.bench_mvp import BenchMvpScenario


def test_end_to_end_synthetic_bench_workflow_produces_pdf_and_dashboard():
    scenario = BenchMvpScenario.synthetic()

    result = scenario.run(
        animal_id="TEST-COW-001",
        limb="REAR_LEFT",
        claw="LATERAL",
        zone="HEEL_BULB",
        lesion="DIGITAL_DERMATITIS",
        treatment="CLEAN_AND_DRESS",
        dressings=1,
        media_refs=("REF:synthetic-before", "REF:synthetic-after"),
        generated_at=datetime(2026, 8, 21, 18, 0, tzinfo=timezone.utc),
    )

    assert result.session["animal_id"] == "TEST-COW-001"
    assert result.dashboard.completed_animals == 1
    assert result.dashboard.consumed_dressings == 1
    assert result.dashboard.banner == "Paweł Humięcki the best zootechnik"
    assert result.pdf_bytes.startswith(b"%PDF-1.4")
    assert b"Synthetic-Test-Only: true" in result.pdf_bytes
    assert result.kvk_observation.simulated is True


def test_ambiguous_identity_fails_closed_before_treatment_commit():
    scenario = BenchMvpScenario.synthetic()
    with pytest.raises(ValueError, match="ambiguous identity"):
        scenario.run_with_identity_candidates(("TEST-COW-001", "TEST-COW-002"))


def test_reference_media_are_explicitly_labeled_and_not_silent_session_evidence():
    scenario = BenchMvpScenario.synthetic()
    result = scenario.run(media_refs=("REF:catalogue-dd-example",))
    assert result.media_refs == ("REF:catalogue-dd-example",)
    assert b"Media-Ref: REF:catalogue-dd-example" in result.pdf_bytes


def test_public_integration_surface_has_no_kvk_command_write_or_actuation_methods():
    forbidden = {"command", "write", "configure", "actuate", "open_gate", "close_gate"}
    public = {name.lower() for name in dir(BenchMvpScenario) if not name.startswith("_")}
    assert public.isdisjoint(forbidden)
