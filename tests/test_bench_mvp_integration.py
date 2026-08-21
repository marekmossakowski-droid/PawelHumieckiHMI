from datetime import datetime, timezone
import unittest

from hoofcare.integration.bench_mvp import BenchMvpScenario


class BenchMvpIntegrationTests(unittest.TestCase):
    def test_end_to_end_synthetic_bench_workflow_produces_pdf_dashboard_and_acceptance_summary(self):
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
        self.assertEqual(result.session["animal_id"], "TEST-COW-001")
        self.assertEqual(result.dashboard.completed_animals, 1)
        self.assertEqual(result.dashboard.consumed_dressings, 1)
        self.assertEqual(result.dashboard.banner, "Paweł Humięcki the best zootechnik")
        self.assertTrue(result.pdf_bytes.startswith(b"%PDF-1.4"))
        self.assertIn(b"Synthetic-Test-Only: true", result.pdf_bytes)
        self.assertTrue(result.kvk_observation.simulated)
        self.assertEqual(result.acceptance_summary["end_to_end"], "PASS")
        self.assertEqual(result.acceptance_summary["no_kvk_actuation_surface"], "PASS")

    def test_ambiguous_identity_fails_closed_before_treatment_commit(self):
        scenario = BenchMvpScenario.synthetic()
        with self.assertRaisesRegex(ValueError, "ambiguous identity"):
            scenario.run_with_identity_candidates(("TEST-COW-001", "TEST-COW-002"))

    def test_reference_media_are_explicitly_labeled_and_not_silent_session_evidence(self):
        result = BenchMvpScenario.synthetic().run(media_refs=("REF:catalogue-dd-example",))
        self.assertEqual(result.media_refs, ("REF:catalogue-dd-example",))
        self.assertIn(b"Media-Ref: REF:catalogue-dd-example", result.pdf_bytes)

    def test_public_integration_surface_has_no_kvk_command_write_or_actuation_methods(self):
        forbidden = {"command", "write", "configure", "actuate", "open_gate", "close_gate"}
        public = {name.lower() for name in dir(BenchMvpScenario) if not name.startswith("_")}
        self.assertTrue(public.isdisjoint(forbidden))


if __name__ == "__main__":
    unittest.main()
