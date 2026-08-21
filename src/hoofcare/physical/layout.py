from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ScreenId(str, Enum):
    DASHBOARD = "DASHBOARD"
    ANIMAL_SESSION = "ANIMAL_SESSION"
    LIMB_CLAW = "LIMB_CLAW"
    ZONE_LESION = "ZONE_LESION"
    TREATMENT = "TREATMENT"
    REPORT_SUMMARY = "REPORT_SUMMARY"


@dataclass(frozen=True)
class TouchTarget:
    control_id: str
    width_px: int
    height_px: int


@dataclass(frozen=True)
class ScreenLayout:
    screen_id: ScreenId
    text_tokens: tuple[str, ...] = ()
    data_bindings: tuple[str, ...] = ()
    control_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class PhysicalHmiLayout:
    panel_class_inch: float
    width_px: int
    height_px: int
    screens: dict[ScreenId, ScreenLayout]
    touch_targets: tuple[TouchTarget, ...]
    isolated_synthetic_only: bool = True
    kvk_connection_allowed: bool = False
    real_farm_data_allowed: bool = False

    @classmethod
    def default(cls) -> "PhysicalHmiLayout":
        screens = {
            ScreenId.DASHBOARD: ScreenLayout(
                ScreenId.DASHBOARD,
                text_tokens=("Paweł Humięcki the best zootechnik",),
                data_bindings=("completed_animals", "consumed_dressings"),
                control_ids=("start_session", "open_reports"),
            ),
            ScreenId.ANIMAL_SESSION: ScreenLayout(
                ScreenId.ANIMAL_SESSION,
                data_bindings=("animal_id", "identity_status"),
                control_ids=("confirm_identity", "cancel_session"),
            ),
            ScreenId.LIMB_CLAW: ScreenLayout(
                ScreenId.LIMB_CLAW,
                data_bindings=("limb", "claw"),
                control_ids=("select_limb", "select_claw", "back"),
            ),
            ScreenId.ZONE_LESION: ScreenLayout(
                ScreenId.ZONE_LESION,
                data_bindings=("zone", "lesion"),
                control_ids=("select_zone", "select_lesion", "back"),
            ),
            ScreenId.TREATMENT: ScreenLayout(
                ScreenId.TREATMENT,
                data_bindings=("treatment", "dressings"),
                control_ids=("select_treatment", "add_dressing", "complete_session", "back"),
            ),
            ScreenId.REPORT_SUMMARY: ScreenLayout(
                ScreenId.REPORT_SUMMARY,
                data_bindings=("report_id", "source_session_id"),
                control_ids=("generate_local_pdf", "back_to_dashboard"),
            ),
        }
        control_ids = tuple(control for screen in screens.values() for control in screen.control_ids)
        targets = tuple(TouchTarget(control_id=control, width_px=64, height_px=64) for control in control_ids)
        return cls(
            panel_class_inch=10.1,
            width_px=1024,
            height_px=600,
            screens=screens,
            touch_targets=targets,
        )
