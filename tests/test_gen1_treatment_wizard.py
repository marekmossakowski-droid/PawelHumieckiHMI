import importlib
from dataclasses import fields
from datetime import date, datetime, timezone
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from hoofcare.application.job_service import JobService
from hoofcare.domain.clinical import (
    CanonicalClinicalRecord,
    LesionRecord,
    MaterialRecord,
    TreatmentRecord,
)
from hoofcare.domain.session import (
    AnimalIdentityResolution,
    Session,
    SessionState,
)
from hoofcare.hmi.workflow import AnatomicalZone, Claw, HMIWorkflow, LesionCode, Limb
from hoofcare.persistence.job_store import LocalJobStore
from hoofcare.persistence.local_store import LocalSessionStore

try:
    from tests.job_fixtures import open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import open_job_fixture


class Gen1TreatmentWizardTests(unittest.TestCase):
    def setUp(self):
        self.module = importlib.import_module("hoofcare.hmi.gen1.treatment_views")
        self.TreatmentStep = self.module.TreatmentStep

    def session(self, *, state=SessionState.IN_PROGRESS):
        return Session(
            session_id="TEST-SESSION-1",
            state=state,
            identity=AnimalIdentityResolution.confirmed("TEST-COW-1"),
            animal_id="TEST-COW-1",
            applied_event_ids=("TEST-IDENTITY-1",),
            treatment_refs=("CLEAN",),
            material_refs=("BLOCK",),
        )

    def workflow(self):
        return (
            HMIWorkflow.synthetic()
            .select_limb(Limb.REAR_LEFT)
            .select_claw(Claw.LATERAL)
            .select_zone(AnatomicalZone.HEEL_BULB)
            .select_lesion(LesionCode.HEEL_HORN_EROSION)
        )

    def clinical_record(self, *, session_id="TEST-SESSION-1", committed=True):
        return CanonicalClinicalRecord(
            record_id="TEST-RECORD-1",
            session_id=session_id,
            animal_id="TEST-COW-1",
            committed_at=datetime(2026, 8, 24, 8, tzinfo=timezone.utc),
            lesion=LesionRecord(
                "HEEL_HORN_EROSION", "Erozja rogu piętki", "HEEL_BULB"
            ),
            treatments=(TreatmentRecord("CLEAN", "Oczyszczenie"),),
            materials=(MaterialRecord("BLOCK", "Klocek", 1.0, "szt."),),
            media=(),
            committed=committed,
            synthetic_test_only=True,
        )

    def project(self, step, **overrides):
        context = {
            "workflow": self.workflow(),
            "clinical_record": self.clinical_record(),
            "follow_up_decided": True,
            "durable_write_ready": True,
        }
        context.update(overrides)
        return self.module.project_treatment_step(self.session(), step, **context)

    def test_pawel_can_complete_every_required_treatment_step_without_camera(self):
        module = importlib.import_module("hoofcare.hmi.workflow")
        self.assertTrue(
            hasattr(module, "complete_synthetic_wizard"),
            "complete_synthetic_wizard must exist",
        )
        steps = tuple(step.value for step in module.complete_synthetic_wizard())
        self.assertEqual(
            steps,
            (
                "IDENTITY",
                "LIMB_CLAW",
                "ZONE_LESION",
                "TREATMENT",
                "MATERIALS",
                "FOLLOW_UP",
                "SUMMARY",
            ),
        )

    def test_every_step_has_polish_projection_and_no_device_action(self):
        for step in self.TreatmentStep:
            with self.subTest(step=step.value):
                view = self.project(step)
                self.assertTrue(view.title_pl)
                self.assertFalse(view.prices_visible)
                self.assertLessEqual(len(view.primary_actions), 4)
                self.assertEqual(
                    tuple(item.action_id for item in view.action_labels_pl),
                    view.primary_actions,
                )
                self.assertTrue(all(item.label_pl for item in view.action_labels_pl))
                self.assertNotIn("camera", view.primary_actions)
                self.assertNotIn("rfid", view.primary_actions)
                self.assertEqual(
                    view.camera_status,
                    "NIEDOSTĘPNE W GENERACJI 1 / AUTHORITY REQUIRED",
                )
                self.assertEqual(
                    view.rfid_status,
                    "NIEDOSTĘPNE W GENERACJI 1 / AUTHORITY REQUIRED",
                )

    def test_complete_cow_is_exposed_only_on_ready_summary(self):
        for step in self.TreatmentStep:
            view = self.project(step)
            if step is self.TreatmentStep.SUMMARY:
                self.assertTrue(view.completion_ready)
                self.assertIn("complete_cow", view.primary_actions)
            else:
                self.assertNotIn("complete_cow", view.primary_actions)

    def test_uncommitted_record_or_failed_durable_prerequisite_routes_to_recovery(self):
        uncommitted = self.project(
            self.TreatmentStep.SUMMARY,
            clinical_record=self.clinical_record(committed=False),
        )
        failed_store = self.project(
            self.TreatmentStep.SUMMARY,
            durable_write_ready=False,
        )

        for view in (uncommitted, failed_store):
            self.assertFalse(view.completion_ready)
            self.assertNotIn("complete_cow", view.primary_actions)
            self.assertIn("open_reconciliation", view.primary_actions)
            self.assertTrue(view.recovery_required)

    def test_follow_up_required_needs_an_explicit_due_date(self):
        session = self.session(state=SessionState.FOLLOW_UP_REQUIRED)
        context = {
            "workflow": self.workflow(),
            "clinical_record": self.clinical_record(),
            "follow_up_decided": True,
            "durable_write_ready": True,
        }

        blocked = self.module.project_treatment_step(
            session,
            self.TreatmentStep.SUMMARY,
            **context,
        )
        ready = self.module.project_treatment_step(
            session,
            self.TreatmentStep.SUMMARY,
            follow_up_due_date=date(2026, 9, 7),
            **context,
        )

        self.assertIn("follow_up_decision", blocked.missing_fields)
        self.assertFalse(blocked.completion_ready)
        self.assertEqual(ready.follow_up_due_date, date(2026, 9, 7))
        self.assertTrue(ready.completion_ready)

    def test_mismatched_clinical_record_fails_closed(self):
        view = self.project(
            self.TreatmentStep.SUMMARY,
            clinical_record=self.clinical_record(session_id="OTHER-SESSION"),
        )

        self.assertIn("canonical_record_match", view.missing_fields)
        self.assertFalse(view.completion_ready)
        self.assertEqual(
            self.module.allowed_treatment_actions(
                self.session(),
                self.TreatmentStep.SUMMARY,
                workflow=self.workflow(),
                clinical_record=self.clinical_record(session_id="OTHER-SESSION"),
                follow_up_decided=True,
                durable_write_ready=True,
            ),
            view.primary_actions,
        )

    def test_mismatched_clinical_codes_fail_closed(self):
        wrong_refs = Session(
            session_id="TEST-SESSION-1",
            state=SessionState.IN_PROGRESS,
            identity=AnimalIdentityResolution.confirmed("TEST-COW-1"),
            animal_id="TEST-COW-1",
            treatment_refs=("OTHER",),
            material_refs=("OTHER",),
        )
        view = self.module.project_treatment_step(
            wrong_refs,
            self.TreatmentStep.SUMMARY,
            workflow=self.workflow(),
            clinical_record=self.clinical_record(),
            follow_up_decided=True,
            durable_write_ready=True,
        )

        self.assertIn("treatment", view.missing_fields)
        self.assertIn("materials", view.missing_fields)
        self.assertFalse(view.completion_ready)

    def test_clinical_selection_must_match_canonical_record(self):
        mismatched_workflow = (
            HMIWorkflow.synthetic()
            .select_limb(Limb.REAR_LEFT)
            .select_claw(Claw.LATERAL)
            .select_zone(AnatomicalZone.TOE)
            .select_lesion(LesionCode.TOE_ULCER)
        )
        view = self.project(
            self.TreatmentStep.SUMMARY,
            workflow=mismatched_workflow,
        )

        self.assertIn("clinical_selection_match", view.missing_fields)
        self.assertFalse(view.completion_ready)

    def test_material_projection_contains_no_price_binding(self):
        view = self.project(self.TreatmentStep.MATERIALS)

        self.assertEqual(
            (view.materials[0].code, view.materials[0].label),
            ("BLOCK", "Klocek"),
        )
        self.assertEqual((view.materials[0].quantity, view.materials[0].unit), (1.0, "szt."))
        self.assertFalse(
            any(field.name.endswith("_grosz") for field in fields(type(view.materials[0])))
        )

    def test_missing_camera_media_does_not_block_ready_summary(self):
        view = self.project(self.TreatmentStep.SUMMARY)

        self.assertEqual(self.clinical_record().media, ())
        self.assertTrue(view.completion_ready)

    def test_projection_rejects_wrong_input_types(self):
        with self.assertRaisesRegex(ValueError, "session must be a Session"):
            self.module.project_treatment_step(object(), self.TreatmentStep.IDENTITY)
        with self.assertRaisesRegex(ValueError, "step must be a TreatmentStep"):
            self.module.project_treatment_step(self.session(), object())
        with self.assertRaisesRegex(ValueError, "workflow must be an HMIWorkflow"):
            self.module.project_treatment_step(
                self.session(), self.TreatmentStep.LIMB_CLAW, workflow=object()
            )

    def test_failed_job_store_leaves_counter_unchanged_and_requires_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs = LocalJobStore(root / "jobs")
            sessions = LocalSessionStore(root / "sessions")
            jobs.save(open_job_fixture())
            service = JobService(jobs, sessions)
            completed = self.session(state=SessionState.COMPLETED)

            with mock.patch.object(jobs, "save", side_effect=OSError("TEST-FAIL")):
                with self.assertRaises(OSError):
                    service.commit_completed_session(
                        "TEST-JOB-1", completed, "TEST-COMPLETION-1"
                    )

            self.assertEqual(jobs.load("TEST-JOB-1").completed_cows, 0)
            self.assertEqual(sessions.load(completed.session_id), completed)
            self.assertEqual(
                service.reconciliation_required(
                    "TEST-JOB-1", (completed.session_id,)
                ),
                (completed.session_id,),
            )


if __name__ == "__main__":
    unittest.main()
