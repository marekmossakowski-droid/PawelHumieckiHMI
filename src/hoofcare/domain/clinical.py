from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


def _require_text(name: str, value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{name} must be non-empty")
    return value


@dataclass(frozen=True)
class LesionRecord:
    code: str
    label: str
    anatomical_zone: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_text("lesion code", self.code))
        object.__setattr__(self, "label", _require_text("lesion label", self.label))
        object.__setattr__(self, "anatomical_zone", _require_text("anatomical_zone", self.anatomical_zone))


@dataclass(frozen=True)
class TreatmentRecord:
    code: str
    label: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_text("treatment code", self.code))
        object.__setattr__(self, "label", _require_text("treatment label", self.label))


@dataclass(frozen=True)
class MaterialRecord:
    code: str
    label: str
    quantity: float
    unit: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _require_text("material code", self.code))
        object.__setattr__(self, "label", _require_text("material label", self.label))
        object.__setattr__(self, "unit", _require_text("material unit", self.unit))
        if self.quantity <= 0:
            raise ValueError("material quantity must be positive")


@dataclass(frozen=True)
class MediaRecord:
    ref: str
    kind: str
    captured_at: datetime
    source: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "ref", _require_text("media ref", self.ref))
        object.__setattr__(self, "kind", _require_text("media kind", self.kind))
        object.__setattr__(self, "source", _require_text("media source", self.source))
        if self.captured_at.tzinfo is None:
            raise ValueError("media captured_at must be timezone-aware")


@dataclass(frozen=True)
class CanonicalClinicalRecord:
    record_id: str
    session_id: str
    animal_id: str
    committed_at: datetime
    lesion: LesionRecord
    treatments: tuple[TreatmentRecord, ...]
    materials: tuple[MaterialRecord, ...]
    media: tuple[MediaRecord, ...] = ()
    committed: bool = False
    synthetic_test_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "record_id", _require_text("record_id", self.record_id))
        object.__setattr__(self, "session_id", _require_text("session_id", self.session_id))
        object.__setattr__(self, "animal_id", _require_text("animal_id", self.animal_id))
        if self.committed_at.tzinfo is None:
            raise ValueError("committed_at must be timezone-aware")
        if not self.treatments:
            raise ValueError("at least one treatment record is required")
        if not self.materials:
            raise ValueError("at least one material record is required")
        if not self.synthetic_test_only:
            raise ValueError("R1 canonical records are synthetic/test-only")
