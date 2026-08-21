from __future__ import annotations

from dataclasses import dataclass, replace

from .layout import PhysicalHmiLayout, ScreenId


@dataclass(frozen=True)
class Widget:
    widget_id: str
    width_px: int = 64
    height_px: int = 64
    interactive: bool = False
    binding: str | None = None
    enabled: bool = True


@dataclass(frozen=True)
class RealizedScreen:
    screen_id: ScreenId
    static_text: tuple[str, ...]
    widgets: tuple[Widget, ...]


@dataclass(frozen=True)
class PhysicalScreenRealization:
    screens: dict[ScreenId, RealizedScreen]
    isolated_synthetic_only: bool = True
    kvk_connection_allowed: bool = False
    real_farm_data_allowed: bool = False

    @classmethod
    def from_layout(cls, layout: PhysicalHmiLayout) -> "PhysicalScreenRealization":
        target_by_id = {target.control_id: target for target in layout.touch_targets}
        screens: dict[ScreenId, RealizedScreen] = {}
        for screen_id, screen in layout.screens.items():
            widgets: list[Widget] = []
            for binding in screen.data_bindings:
                widgets.append(Widget(widget_id=f"display_{binding}", interactive=False, binding=binding))
            for control_id in screen.control_ids:
                target = target_by_id[control_id]
                widgets.append(
                    Widget(
                        widget_id=control_id,
                        width_px=target.width_px,
                        height_px=target.height_px,
                        interactive=True,
                    )
                )
            screens[screen_id] = RealizedScreen(
                screen_id=screen_id,
                static_text=screen.text_tokens,
                widgets=tuple(widgets),
            )
        return cls(screens=screens)

    def render(self, screen_id: ScreenId, state: dict[str, object] | None = None) -> RealizedScreen:
        state = state or {}
        screen = self.screens[screen_id]
        widgets = screen.widgets
        if screen_id is ScreenId.ANIMAL_SESSION and state.get("identity_status") in {"AMBIGUOUS", "CONFLICTING", "UNKNOWN"}:
            widgets = tuple(
                replace(widget, enabled=False) if widget.widget_id == "confirm_identity" else widget
                for widget in widgets
            )
        return replace(screen, widgets=widgets)
