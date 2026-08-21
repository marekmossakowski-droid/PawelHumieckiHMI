from __future__ import annotations

from dataclasses import dataclass

from .layout import ScreenId


class NavigationError(RuntimeError):
    pass


@dataclass
class PhysicalNavigationController:
    current_screen: ScreenId = ScreenId.DASHBOARD
    identity_status: str = "UNKNOWN"
    isolated_synthetic_only: bool = True
    kvk_connection_allowed: bool = False
    real_farm_data_allowed: bool = False
    _limb_selected: bool = False
    _claw_selected: bool = False
    _zone_selected: bool = False
    _lesion_selected: bool = False
    _treatment_selected: bool = False

    @classmethod
    def default(cls) -> "PhysicalNavigationController":
        return cls()

    def bind_identity_status(self, status: str) -> None:
        normalized = str(status).strip().upper()
        self.identity_status = normalized if normalized else "UNKNOWN"

    def activate(self, action: str) -> None:
        if action in {"open_valve", "kvk_command", "plc_write", "motor_start"}:
            raise NavigationError("machine-control actions are outside IA-HC-002")

        if self.current_screen is ScreenId.DASHBOARD:
            if action == "start_session":
                self.current_screen = ScreenId.ANIMAL_SESSION
                return
            self._reject(action)

        if self.current_screen is ScreenId.ANIMAL_SESSION:
            if action == "confirm_identity":
                if self.identity_status != "CONFIRMED":
                    raise NavigationError("identity must be CONFIRMED before advancing")
                self.current_screen = ScreenId.LIMB_CLAW
                return
            if action == "cancel_session":
                self._reset_to_dashboard()
                return
            self._reject(action)

        if self.current_screen is ScreenId.LIMB_CLAW:
            if action == "select_limb":
                self._limb_selected = True
                return
            if action == "select_claw":
                if not self._limb_selected:
                    raise NavigationError("limb selection is required before claw selection")
                self._claw_selected = True
                self.current_screen = ScreenId.ZONE_LESION
                return
            self._reject(action)

        if self.current_screen is ScreenId.ZONE_LESION:
            if action == "select_zone":
                self._zone_selected = True
                return
            if action == "select_lesion":
                if not self._zone_selected:
                    raise NavigationError("zone selection is required before lesion selection")
                self._lesion_selected = True
                self.current_screen = ScreenId.TREATMENT
                return
            self._reject(action)

        if self.current_screen is ScreenId.TREATMENT:
            if action == "select_treatment":
                if not self._lesion_selected:
                    raise NavigationError("lesion selection is required before treatment")
                self._treatment_selected = True
                return
            if action == "add_dressing":
                if not self._treatment_selected:
                    raise NavigationError("treatment selection is required before material entry")
                return
            if action == "complete_session":
                if not self._treatment_selected:
                    raise NavigationError("treatment selection is required before completion")
                self.current_screen = ScreenId.REPORT_SUMMARY
                return
            self._reject(action)

        if self.current_screen is ScreenId.REPORT_SUMMARY:
            if action == "back_to_dashboard":
                self._reset_to_dashboard()
                return
            if action == "generate_local_pdf":
                return
            self._reject(action)

        self._reject(action)

    def _reset_to_dashboard(self) -> None:
        self.current_screen = ScreenId.DASHBOARD
        self.identity_status = "UNKNOWN"
        self._limb_selected = False
        self._claw_selected = False
        self._zone_selected = False
        self._lesion_selected = False
        self._treatment_selected = False

    @staticmethod
    def _reject(action: str) -> None:
        raise NavigationError(f"action not allowed in current screen: {action}")
