from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionEvent, SessionEventType, SessionState
from hoofcare.physical.acceptance import PhysicalPrototypeAcceptance
from hoofcare.physical.persistence_reporting import PhysicalPersistenceReportingValidator


@dataclass(frozen=True)
class DurableAcceptanceResult:
    status: str
    checks: dict[str, str]
    report_pdf: bytes


class DurablePhysicalPrototypeAcceptance:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.base = PhysicalPrototypeAcceptance.synthetic(self.root)
        self.persistence = PhysicalPersistenceReportingValidator(self.root)

    @classmethod
    def synthetic(cls, root: Path) -> "DurablePhysicalPrototypeAcceptance":
        return cls(root)

    def run(self) -> DurableAcceptanceResult:
        checks: dict[str, str] = {}
        checks["screen_layout"] = "PASS" if self.base._screen_layout_ok() else "FAIL"
        checks["navigation"] = "PASS" if self.base._navigation_ok() else "FAIL"

        session = Session.new().apply(
            SessionEvent(
                event_id="R0C:identity",
                event_type=SessionEventType.IDENTITY_RESOLVED,
                payload=AnimalIdentityResolution.confirmed("TEST-COW-R0C-001"),
            )
        )
        completed = self.persistence.complete_and_commit(session, event_id="R0C:complete")
        checks["durable_completion"] = "PASS" if completed.state is SessionState.COMPLETED else "FAIL"

        recovered = self.persistence.recover_session(completed.session_id)
        checks["persistence_restart"] = "PASS" if recovered == completed else "FAIL"

        report = self.persistence.build_local_report(
            completed.session_id,
            report_id=f"R0C-{completed.session_id}",
            generated_at=datetime.now(timezone.utc),
            lesion_summary="DIGITAL_DERMATITIS",
            treatment_summary="CLEAN_AND_DRESS",
            material_summary="dressings=1",
        )
        pdf = report.to_pdf_bytes()
        checks["local_report"] = "PASS" if (
            report.source_session_id == completed.session_id
            and pdf.startswith(b"%PDF-1.4")
            and b"xref" in pdf
            and b"trailer" in pdf
            and pdf.rstrip().endswith(b"%%EOF")
        ) else "FAIL"
        checks["synthetic_only"] = "PASS" if self.persistence.synthetic_test_only and report.synthetic_test_only else "FAIL"
        checks["no_kvk_connection"] = "PASS" if (
            not self.base.layout.kvk_connection_allowed
            and not self.base.navigation.kvk_connection_allowed
            and not self.persistence.kvk_connection_allowed
        ) else "FAIL"
        checks["restricted_action_surface"] = "PASS" if self.base._machine_control_surface_absent() else "FAIL"

        status = "PASS" if checks and all(value == "PASS" for value in checks.values()) else "FAIL"
        return DurableAcceptanceResult(status=status, checks=checks, report_pdf=pdf)
