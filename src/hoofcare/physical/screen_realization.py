from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .layout import PhysicalHmiLayout, ScreenId


class WidgetKind(str, Enum):
    LABEL = "LABEL"
    VALUE = "VALUE"
    BUTTON = "BUTTON"


@dataclass(frozen=True)
class PhysicalWidget:
    widget_id: str
    kind: WidgetKind
    width_px: int
    height_px: int
    text: str | None = None
    binding: str | None = None
    action: str | None = None


@dataclass(frozen=True)
class PhysicalScreen:
    screen_id: ScreenId
    widgets: tuple[PhysicalWidget, ...]


@dataclass(frozen=True)
class PhysicalScreenRealization:
    screens: dict[ScreenId, PhysicalScreen]
    isolated_synthetic_only: bool = True
    kvk_connection_allowed: bool = False
    real_farm_data_allowed: bool = False

    @classmethod
    def default(cls) -> "PhysicalScreenRealization":
        layout = PhysicalHmiLayout.default()
        target_by_control = {target.control_id: target for target in layout.touch_targets}
        screens: dict[ScreenId, PhysicalScreen] = {}

        for screen_id, screen_layout in layout.screens.items():
            widgets: list[PhysicalWidget] = []
            for index, text in enumerate(screen_layout.text_tokens):
                widgets.append(
                    PhysicalWidget(
                        widget_id=f"{screen_id.value.lower()}_text_{index}",
                        kind=WidgetKind.LABEL,
                        width_px=320,
                        height_px=48,
                        text=text,
                    )
                )
            for binding in screen_layout.data_bindings:
                widgets.append(
                    PhysicalWidget(
                        widget_id=f"{screen_id.value.lower()}_{binding}",
                        kind=WidgetKind.VALUE,
                        width_px=160,
                        height_px=48,
                        binding=binding,
                    )
                )
            for control_id in screen_layout.control_ids:
                target = target_by_control[control_id]
                widgets.append(
                    PhysicalWidget(
                        widget_id=f"{screen_id.value.lower()}_{control_id}",
                        kind=WidgetKind.BUTTON,
                        width_px=target.width_px,
                        height_px=target.height_px,
                        text=control_id.replace("_", " ").title(),
                        action=control_id,
                    )
                )
            screens[screen_id] = PhysicalScreen(screen_id=screen_id, widgets=tuple(widgets))

        return cls(screens=screens)
