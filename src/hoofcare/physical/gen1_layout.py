from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from hoofcare.hmi.gen1.navigation import Gen1Route


_COLOR_TOKENS = MappingProxyType(
    {
        "surface.canvas": "#F2F4F7",
        "surface.card": "#FFFFFF",
        "surface.selected": "#E8F1FF",
        "text.primary": "#17212B",
        "text.secondary": "#5F6B7A",
        "action.primary": "#1477FF",
        "action.disabled": "#C7CDD5",
        "status.success": "#168A5B",
        "status.warning": "#A85F00",
        "status.blocked": "#C9363E",
        "assist.teal": "#168F84",
        "assist.violet": "#665CF6",
        "border.subtle": "#D8DEE6",
    }
)


@dataclass(frozen=True)
class AdaptiveRegion:
    region_id: str
    x: int
    y: int
    width: int
    height: int

    def within(self, canvas_width: int, canvas_height: int) -> bool:
        return (
            self.x >= 0
            and self.y >= 0
            and self.width > 0
            and self.height > 0
            and self.x + self.width <= canvas_width
            and self.y + self.height <= canvas_height
        )


@dataclass(frozen=True)
class TouchTarget:
    action_id: str
    label_pl: str
    x: int
    y: int
    width: int
    height: int

    def within(self, canvas_width: int, canvas_height: int) -> bool:
        return (
            self.x >= 0
            and self.y >= 0
            and self.width > 0
            and self.height > 0
            and self.x + self.width <= canvas_width
            and self.y + self.height <= canvas_height
        )

    def overlaps(self, other: "TouchTarget") -> bool:
        return not (
            self.x + self.width <= other.x
            or other.x + other.width <= self.x
            or self.y + self.height <= other.y
            or other.y + other.height <= self.y
        )


@dataclass(frozen=True)
class Gl100eScreen:
    route: Gen1Route
    label_pl: str
    regions: tuple[AdaptiveRegion, ...]
    targets: tuple[TouchTarget, ...]

    def within_canvas(self, width: int, height: int) -> bool:
        return all(region.within(width, height) for region in self.regions) and all(
            target.within(width, height) for target in self.targets
        )

    def has_overlaps(self) -> bool:
        return any(
            first.overlaps(second)
            for index, first in enumerate(self.targets)
            for second in self.targets[index + 1 :]
        )


_ROUTE_PRESENTATION: dict[Gen1Route, tuple[str, tuple[tuple[str, str], ...]]] = {
    Gen1Route.START_RECOVERY: (
        "Start i odzyskiwanie",
        (("open_dashboard", "Pulpit"), ("open_reconciliation", "Uzgodnij"), ("open_diagnostics", "Diagnostyka")),
    ),
    Gen1Route.OPERATOR_DASHBOARD: (
        "Pulpit Pawła",
        (("new_job", "Nowe zlecenie"), ("resume_job", "Wznów pracę"), ("open_statistics", "Statystyki"), ("open_owner_pin", "Właściciel")),
    ),
    Gen1Route.JOB_SELECTION: ("Wybór zlecenia", (("open_job_pricing", "Dalej"), ("back", "Wstecz"))),
    Gen1Route.JOB_PRICING: ("Otwarcie i ceny", (("confirm_job", "Zatwierdź"), ("back", "Wstecz"))),
    Gen1Route.PRICE_CORRECTION: ("Korekta ceny", (("save_correction", "Zapisz"), ("back", "Anuluj"))),
    Gen1Route.ANIMAL_IDENTITY: ("Identyfikacja zwierzęcia", (("next", "Dalej"), ("cancel", "Anuluj"))),
    Gen1Route.LIMB_CLAW: ("Kończyna i racica", (("next", "Dalej"), ("back", "Wstecz"))),
    Gen1Route.ZONE_LESION: ("Strefa i zmiana", (("next", "Dalej"), ("back", "Wstecz"))),
    Gen1Route.TREATMENT: ("Zabieg", (("next", "Dalej"), ("back", "Wstecz"))),
    Gen1Route.MATERIALS: ("Materiały", (("next", "Dalej"), ("back", "Wstecz"))),
    Gen1Route.FOLLOW_UP: ("Termin kontroli", (("next", "Dalej"), ("back", "Wstecz"))),
    Gen1Route.COW_SUMMARY: ("Podsumowanie krowy", (("complete_cow", "Ukończ"), ("open_reconciliation", "Uzgodnij"), ("back", "Wstecz"))),
    Gen1Route.WORK_STATISTICS: ("Statystyki pracy", (("open_history", "Historia"), ("back", "Pulpit"))),
    Gen1Route.JOB_HISTORY: ("Historia zleceń", (("open_settlement", "Rozliczenie"), ("back", "Wstecz"))),
    Gen1Route.JOB_CLOSURE: ("Zamknięcie zlecenia", (("correct_price", "Korekta ceny"), ("confirm_close", "Zamknij"), ("back", "Wstecz"))),
    Gen1Route.CLOSED_SETTLEMENT: ("Zamknięte rozliczenie", (("open_history", "Historia"), ("back", "Pulpit"))),
    Gen1Route.OWNER_PIN: ("PIN właściciela", (("unlock", "Odblokuj"), ("cancel", "Anuluj"))),
    Gen1Route.OWNER_DASHBOARD: ("Pulpit właściciela", (("open_owner_admin", "Administracja"), ("open_history", "Historia"), ("open_diagnostics", "Diagnostyka"), ("back", "Pulpit Pawła"))),
    Gen1Route.LOCAL_ADMIN: ("Administracja lokalna", (("back", "Wstecz"),)),
    Gen1Route.DIAGNOSTICS: ("Diagnostyka", (("back", "Wstecz"),)),
    Gen1Route.RECONCILIATION: ("Uzgodnienie i błąd", (("retry", "Ponów"), ("open_diagnostics", "Diagnostyka"), ("back", "Wstecz"))),
}


def _targets(actions: tuple[tuple[str, str], ...]) -> tuple[TouchTarget, ...]:
    target_width = 232
    gap = 16
    total_width = len(actions) * target_width + max(0, len(actions) - 1) * gap
    start_x = (1024 - total_width) // 2
    return tuple(
        TouchTarget(action_id, label, start_x + index * (target_width + gap), 536, target_width, 64)
        for index, (action_id, label) in enumerate(actions)
    )


@dataclass(frozen=True)
class Gl100eProfile:
    profile_id: str
    visual_system_id: str
    color_tokens: Mapping[str, str]
    width: int
    height: int
    header: AdaptiveRegion
    content: AdaptiveRegion
    action_bar: AdaptiveRegion
    screens: tuple[Gl100eScreen, ...]
    synthetic_only: bool = True
    device_access_allowed: bool = False

    @classmethod
    def default(cls) -> "Gl100eProfile":
        header = AdaptiveRegion("header", 0, 0, 1024, 64)
        content = AdaptiveRegion("content", 0, 64, 1024, 472)
        action_bar = AdaptiveRegion("action_bar", 0, 536, 1024, 64)
        regions = (header, content, action_bar)
        screens = tuple(
            Gl100eScreen(route, _ROUTE_PRESENTATION[route][0], regions, _targets(_ROUTE_PRESENTATION[route][1]))
            for route in Gen1Route
        )
        return cls(
            profile_id="gl100e-landscape-v1",
            visual_system_id="UX-HC-002-A1/G1-LIGHT-A",
            color_tokens=_COLOR_TOKENS,
            width=1024,
            height=600,
            header=header,
            content=content,
            action_bar=action_bar,
            screens=screens,
        )
