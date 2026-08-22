from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionEvent, SessionEventType
from hoofcare.physical.layout import PhysicalHmiLayout, ScreenId
from hoofcare.physical.navigation import NavigationError, PhysicalNavigationController
from hoofcare.physical.persistence_reporting import PhysicalPersistenceReportingValidator


@dataclass(frozen=True)
class PhysicalPrototypeAcceptanceResult:
    status: str
    checks: dict[str, str]
    report_pdf: bytes
    field_kvk_verified: bool = False
    real_farm_data_used: bool = False
    deployment_ready: bool = False


class PhysicalPrototypeAcceptance:
    _FORBIDDEN_ACTIONS = {"open_valve", "kvk_command", "plc_write", "motor_start"}

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.layout = PhysicalHmiLayout.default()
        self.navigation = PhysicalNavigationController.default()
        self.persistence = PhysicalPersistenceReportingValidator(self.root)

    @classmethod
    def synthetic(cls, root: Path) -> "PhysicalPrototypeAcceptance":
        return cls(root)

    def assert_action_allowed(self, action: str) -> None:
        if action in self._FORBIDDEN_ACTIONS:
            raise ValueError("machine-control action is outside IA-HC-002")

    def run(self) -> PhysicalPrototypeAcceptanceResult:
        checks: dict[str, str] = {}

        checks["screen_layout"] = "PASS" if self._screen_layout_ok() else "FAIL"
        checks["navigation"] = "PASS" if self._navigation_ok() else "FAIL"

        session = Session.new().apply(
            SessionEvent(
                event_id="P7:identity",
                event_type=SessionEventType.IDENTITY_RESOLVED,
                payload=AnimalIdentityResolution.confirmed("TEST-COW-P7-001"),
            )
        )
        session = session.apply(SessionEvent(event_id="P7:complete", event_type=SessionEventType.COMPLETE))
        self.persistence.commit_session(session)
        recovered = self.persistence.recover_session(session.session_id)
        checks["persistence_restart"] = "PASS" if recovered == session else "FAIL"

        report = self.persistence.build_local_report(
            session.session_id,
            report_id=f"P7-{session.session_id}",
            generated_at=datetime.now(timezone.utc),
            lesion_summary="DIGITAL_DERMATITIS",
            treatment_summary="CLEAN_AND_DRESS",
            material_summary="dressings=1",
        )
        pdf = report.to_pdf_bytes()
        checks["local_report"] = "PASS" if pdf.startswith(b"%PDF-1.4") and report.source_session_id == session.session_id else "FAIL"
        checks["synthetic_only"] = "PASS" if self.persistence.synthetic_test_only and report.synthetic_test_only else "FAIL"
        checks["no_kvk_connection"] = "PASS" if not self.layout.kvk_connection_allowed and not self.navigation.kvk_connection_allowed and not self.persistence.kvk_connection_allowed else "FAIL"
        checks["no_machine_control_surface"] = "PASS" if self._machine_control_surface_absent() else "FAIL"

        status = "PASS" if all(value == "PASS" for value in checks.values()) else "FAIL"
        return PhysicalPrototypeAcceptanceResult(status=status, checks=checks, report_pdf=pdf)

    def _screen_layout_ok(self) -> bool:
        required = {
            ScreenId.DASHBOARD,
            ScreenId.ANIMAL_SESSION,
            ScreenId.LIMB_CLAW,
            ScreenId.ZONE_LESION,
            ScreenId.TREATMENT,
            ScreenId.REPORT_SUMMARY,
        }
        return (
            self.layout.panel_class_inch == 10.1
            and self.layout.width_px == 1024
            and self.layout.height_px == 600
            and required.issubset(self.layout.screens)
            and all(target.width_px >= 48 and target.height_px >= 48 for target in self.layout.touch_targets)
        )

    def _navigation_ok(self) -> bool:
        nav = PhysicalNavigationController.default()
        try:
            nav.activate("start_session")
            nav.bind_identity_status("CONFIRMED")
            nav.activate("confirm_identity")
            nav.activate("select_limb")
            nav.activate("select_claw")
            nav.activate("select_zone")
            nav.activate("select_lesion")
            nav.activate("select_treatment")
            nav.activate("add_dressing")
            nav.activate("complete_session")
        except NavigationError:
            return False
        return nav.current_screen is ScreenId.REPORT_SUMMARY

    def _machine_control_surface_absent(self) -> bool:
        controls = {control for screen in self.layout.screens.values() for control in screen.control_ids}
        if controls & self._FORBIDDEN_ACTIONS:
            return False
        for action in self._FORBIDDEN_ACTIONS:
            try:
                self.navigation.activate(action)
            except NavigationError:
                continue
            return False
        return True
