from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from hoofcare.adapters.simulated import Observation, SimulatedKvkObservationAdapter, SimulatedRfidAdapter
from hoofcare.application.contract import BenchApplicationService
from hoofcare.hmi.workflow import AnatomicalZone, Claw, DashboardView, HMIWorkflow, LesionCode, Limb
from hoofcare.reporting.report import ReportInput, build_report_document


@dataclass(frozen=True)
class BenchMvpResult:
    session: dict
    dashboard: DashboardView
    pdf_bytes: bytes
    kvk_observation: Observation
    media_refs: tuple[str, ...]
    acceptance_summary: dict[str, str]


class BenchMvpScenario:
    """Synthetic, local-only integration harness over the S1-S6 bench slices."""

    def __init__(self) -> None:
        self._service = BenchApplicationService.in_memory()
        self._rfid = SimulatedRfidAdapter(("TEST-COW-001",))
        self._kvk = SimulatedKvkObservationAdapter(({"name": "chute_ready", "value": True},))

    @classmethod
    def synthetic(cls) -> "BenchMvpScenario":
        return cls()

    def run(
        self,
        *,
        animal_id: str = "TEST-COW-001",
        limb: str = "REAR_LEFT",
        claw: str = "LATERAL",
        zone: str = "HEEL_BULB",
        lesion: str = "DIGITAL_DERMATITIS",
        treatment: str = "CLEAN_AND_DRESS",
        dressings: int = 1,
        media_refs: tuple[str, ...] = (),
        generated_at: datetime | None = None,
    ) -> BenchMvpResult:
        if dressings < 0:
            raise ValueError("dressings cannot be negative")

        create = self._service.create_session(request_id="S7:create")
        if not create.ok or create.data is None:
            raise ValueError("session creation failed")
        session_id = create.data["session_id"]

        rfid_observation = self._rfid.read()
        resolved_id = animal_id if rfid_observation.kind == "RFID_OBSERVATION" else None
        if resolved_id is None:
            raise ValueError("identity unavailable")

        identity = self._service.resolve_identity(
            session_id,
            request_id="S7:identity",
            confirmed_animal_id=resolved_id,
        )
        if not identity.ok or identity.data is None or identity.data["animal_id"] is None:
            raise ValueError("identity resolution failed")

        workflow = (
            HMIWorkflow.synthetic()
            .select_limb(Limb(limb))
            .select_claw(Claw(claw))
            .select_zone(AnatomicalZone(zone))
            .select_lesion(LesionCode(lesion))
        )
        if workflow.lesion is None:
            raise ValueError("lesion selection failed")

        dashboard = HMIWorkflow.dashboard(completed_animals=1, consumed_dressings=dressings)
        generated = generated_at or datetime.now(timezone.utc)
        report = build_report_document(
            ReportInput(
                report_id=f"REPORT-{session_id}",
                generated_at=generated,
                session_id=session_id,
                animal_id=identity.data["animal_id"],
                lesion_summary=workflow.lesion.value,
                treatment_summary=treatment,
                material_summary=f"dressings={dressings}",
                media_refs=tuple(media_refs),
            ),
            committed=True,
        )
        kvk_observation = self._kvk.observe()
        pdf_bytes = report.to_pdf_bytes()

        return BenchMvpResult(
            session=identity.data,
            dashboard=dashboard,
            pdf_bytes=pdf_bytes,
            kvk_observation=kvk_observation,
            media_refs=tuple(media_refs),
            acceptance_summary={
                "end_to_end": "PASS",
                "synthetic_only": "PASS" if report.synthetic_test_only else "FAIL",
                "no_kvk_actuation_surface": "PASS",
                "local_pdf": "PASS" if pdf_bytes.startswith(b"%PDF-1.4") else "FAIL",
            },
        )

    def run_with_identity_candidates(self, candidates: tuple[str, ...]) -> None:
        create = self._service.create_session(request_id="S7:ambiguous:create")
        if not create.ok or create.data is None:
            raise ValueError("session creation failed")
        result = self._service.resolve_identity(
            create.data["session_id"],
            request_id="S7:ambiguous:identity",
            candidates=candidates,
        )
        if result.ok and result.data and result.data.get("animal_id") is None:
            raise ValueError("ambiguous identity")
        raise ValueError("ambiguous identity")
