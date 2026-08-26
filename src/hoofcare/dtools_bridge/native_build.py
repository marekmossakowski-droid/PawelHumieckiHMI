from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NativeDToolsWidget:
    widget_id: str
    label_pl: str
    widget_type: str
    primary_action: bool
    geometry: tuple[int, int, int, int]
    binding_id: str
    value_type: str
    direction: str
    available_when: str
    missing_data: str
    use_case_id: str | None = None


@dataclass(frozen=True)
class NativeDToolsScreen:
    screen_id: str
    route_id: str
    label_pl: str
    widgets: tuple[NativeDToolsWidget, ...]


@dataclass(frozen=True)
class NativeDToolsBuildPlan:
    project_name: str
    canvas: tuple[int, int]
    screens: tuple[NativeDToolsScreen, ...]
    source_sha256: str

    @classmethod
    def from_manifest(cls, path: Path) -> "NativeDToolsBuildPlan":
        source = path.read_text(encoding="utf-8")
        return cls.from_json(source)

    @classmethod
    def from_json(cls, source: str) -> "NativeDToolsBuildPlan":
        document = json.loads(source)
        canvas = document["canvas"]
        width = _positive_int(canvas["width"], "INVALID_CANVAS_WIDTH")
        height = _positive_int(canvas["height"], "INVALID_CANVAS_HEIGHT")

        screens: list[NativeDToolsScreen] = []
        seen_screen_ids: set[str] = set()
        for raw_screen in document["screens"]:
            screen_id = str(raw_screen["screen_id"])
            if screen_id in seen_screen_ids:
                raise ValueError(f"DUPLICATE_SCREEN_ID:{screen_id}")
            seen_screen_ids.add(screen_id)

            widgets = tuple(
                _materialize_widget(raw_widget, screen_id, width, height)
                for raw_widget in raw_screen["widgets"]
            )
            screens.append(
                NativeDToolsScreen(
                    screen_id=screen_id,
                    route_id=str(raw_screen["route_id"]),
                    label_pl=str(raw_screen["label_pl"]),
                    widgets=widgets,
                )
            )

        return cls(
            project_name="HoofCare_GL100E_G1",
            canvas=(width, height),
            screens=tuple(screens),
            source_sha256=sha256(source.encode("utf-8")).hexdigest(),
        )


def _positive_int(value: Any, error_code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(error_code)
    return value


def _materialize_widget(
    raw_widget: dict[str, Any],
    screen_id: str,
    canvas_width: int,
    canvas_height: int,
) -> NativeDToolsWidget:
    geometry = raw_widget["geometry"]
    x = geometry["x"]
    y = geometry["y"]
    width = geometry["width"]
    height = geometry["height"]
    coordinates = (x, y, width, height)
    if (
        any(isinstance(value, bool) or not isinstance(value, int) for value in coordinates)
        or x < 0
        or y < 0
        or width <= 0
        or height <= 0
        or x + width > canvas_width
        or y + height > canvas_height
    ):
        raise ValueError(
            f"WIDGET_OUT_OF_BOUNDS:{screen_id}:{raw_widget['widget_id']}"
        )

    binding = raw_widget["binding"]
    return NativeDToolsWidget(
        widget_id=str(raw_widget["widget_id"]),
        label_pl=str(raw_widget["label_pl"]),
        widget_type=str(raw_widget["widget_type"]),
        primary_action=bool(raw_widget["primary_action"]),
        geometry=coordinates,
        binding_id=str(binding["binding_id"]),
        value_type=str(binding["value_type"]),
        direction=str(binding["direction"]),
        available_when=str(binding["available_when"]),
        missing_data=str(binding["missing_data"]),
        use_case_id=(
            str(binding["use_case_id"]) if "use_case_id" in binding else None
        ),
    )
