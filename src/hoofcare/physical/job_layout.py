from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobTouchTarget:
    control_id: str
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Gl100eJobLayout:
    width_px: int
    height_px: int
    touch_targets: tuple[JobTouchTarget, ...]

    @classmethod
    def default(cls) -> "Gl100eJobLayout":
        return cls(
            width_px=1024,
            height_px=600,
            touch_targets=(
                JobTouchTarget("back", 62, 500, 180, 64),
                JobTouchTarget("correct_price", 282, 500, 180, 64),
                JobTouchTarget("confirm", 502, 500, 180, 64),
                JobTouchTarget("next", 722, 500, 180, 64),
            ),
        )
