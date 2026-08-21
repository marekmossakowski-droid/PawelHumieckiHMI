from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from hoofcare.domain.session import Session, SessionState
from hoofcare.physical.prototype_validation import PhysicalPrototypeValidator


_MACHINE_CONTROL_ACTIONS = {
    "open_valve",
    "kvk_command",
    "plc_write",
    "motor_start",
}


@dataclass(frozen=True)
class PhysicalAcceptanceSummary:
    accepted: bool
    restart_recovery_verified: bool
    canonical_pdf_verified: bool
    negative_controls_verified: bool
    kvk_connection_allowed: bool
    real_farm_data_allowed: bool
    pdf_bytes: bytes


class PhysicalPrototypeAcceptance:
    """Synthetic-only acceptance harness for isolated physical prototype closure readiness."""

    kvk_connection_allowed = False
    real_farm_data_allowed = False

    def __init__(self, root: Path) -> None:
        self._validator = PhysicalPrototypeValidator(Path(root))

    def assert_operator_action_allowed(self, action: str) -> None:
        if str(action).strip().lower() in _MACHINE_CONTROL_ACTIONS:
            raise ValueError("machine-control actions are outside IA-HC-002")

    def run(
        self,
        session: Session,
        *,
        report_id: str,
        generated_at: datetime,
    ) -> PhysicalAcceptanceSummary:
        if session.state is not SessionState.COMPLETED or not session.animal_id:
            raise ValueError("acceptance requires a completed session with confirmed identity")

        self._validator.commit_session(session)
        recovered = self._validator.recover_session(session.session_id)
        if recovered != session:
            raise ValueError("restart recovery did not reproduce committed canonical session")

        pdf_bytes = self._validator.generate_report(
            session.session_id,
            report_id=report_id,
            generated_at=generated_at,
            lesion_summary="synthetic acceptance lesion",
            treatment_summary="synthetic acceptance treatment",
            material_summary="synthetic acceptance materials",
        )
        canonical_pdf_verified = (
            pdf_bytes.startswith(b"%PDF-1.4")
            and f"Source-Session-ID: {session.session_id}".encode("utf-8") in pdf_bytes
            and b"Synthetic-Test-Only: true" in pdf_bytes
        )
        if not canonical_pdf_verified:
            raise ValueError("canonical local PDF verification failed")

        for action in _MACHINE_CONTROL_ACTIONS:
            try:
                self.assert_operator_action_allowed(action)
            except ValueError:
                continue
            raise ValueError(f"negative control unexpectedly allowed: {action}")

        return PhysicalAcceptanceSummary(
            accepted=True,
            restart_recovery_verified=True,
            canonical_pdf_verified=True,
            negative_controls_verified=True,
            kvk_connection_allowed=False,
            real_farm_data_allowed=False,
            pdf_bytes=pdf_bytes,
        )
