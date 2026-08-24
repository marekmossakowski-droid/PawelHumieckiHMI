from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class Limb(str, Enum):
    FRONT_LEFT = "FRONT_LEFT"
    FRONT_RIGHT = "FRONT_RIGHT"
    REAR_LEFT = "REAR_LEFT"
    REAR_RIGHT = "REAR_RIGHT"


class Claw(str, Enum):
    MEDIAL = "MEDIAL"
    LATERAL = "LATERAL"


class AnatomicalZone(str, Enum):
    TOE = "TOE"
    SOLE = "SOLE"
    WHITE_LINE = "WHITE_LINE"
    AXIAL_WALL = "AXIAL_WALL"
    ABAXIAL_WALL = "ABAXIAL_WALL"
    HEEL_BULB = "HEEL_BULB"
    SOFT_HEEL_TISSUE = "SOFT_HEEL_TISSUE"
    INTERDIGITAL_SPACE = "INTERDIGITAL_SPACE"


class LesionCode(str, Enum):
    DIGITAL_DERMATITIS = "DIGITAL_DERMATITIS"
    INTERDIGITAL_DERMATITIS = "INTERDIGITAL_DERMATITIS"
    INTERDIGITAL_PHLEGMON = "INTERDIGITAL_PHLEGMON"
    HEEL_HORN_EROSION = "HEEL_HORN_EROSION"
    SOLE_ULCER = "SOLE_ULCER"
    WHITE_LINE_DISEASE = "WHITE_LINE_DISEASE"
    TOE_ULCER = "TOE_ULCER"
    OTHER_OPERATOR_CLASSIFIED = "OTHER_OPERATOR_CLASSIFIED"


class WorkflowStep(str, Enum):
    LIMB = "LIMB"
    CLAW = "CLAW"
    ZONE = "ZONE"
    LESION = "LESION"
    TREATMENT = "TREATMENT"


class TreatmentStep(str, Enum):
    IDENTITY = "IDENTITY"
    LIMB_CLAW = "LIMB_CLAW"
    ZONE_LESION = "ZONE_LESION"
    TREATMENT = "TREATMENT"
    MATERIALS = "MATERIALS"
    FOLLOW_UP = "FOLLOW_UP"
    SUMMARY = "SUMMARY"


def complete_synthetic_wizard() -> tuple[TreatmentStep, ...]:
    return tuple(TreatmentStep)


@dataclass(frozen=True)
class DashboardView:
    banner: str
    completed_animals: int
    consumed_dressings: int

    def __post_init__(self) -> None:
        if self.completed_animals < 0 or self.consumed_dressings < 0:
            raise ValueError("dashboard counters cannot be negative")


@dataclass(frozen=True)
class HMIWorkflow:
    step: WorkflowStep = WorkflowStep.LIMB
    limb: Limb | None = None
    claw: Claw | None = None
    zone: AnatomicalZone | None = None
    lesion: LesionCode | None = None

    @classmethod
    def synthetic(cls) -> "HMIWorkflow":
        return cls()

    @staticmethod
    def dashboard(*, completed_animals: int, consumed_dressings: int) -> DashboardView:
        return DashboardView(
            banner="Paweł Humięcki the best zootechnik",
            completed_animals=completed_animals,
            consumed_dressings=consumed_dressings,
        )

    def select_limb(self, limb: Limb) -> "HMIWorkflow":
        self._require_step(WorkflowStep.LIMB)
        return replace(self, limb=limb, step=WorkflowStep.CLAW)

    def select_claw(self, claw: Claw) -> "HMIWorkflow":
        self._require_step(WorkflowStep.CLAW)
        return replace(self, claw=claw, step=WorkflowStep.ZONE)

    def select_zone(self, zone: AnatomicalZone) -> "HMIWorkflow":
        self._require_step(WorkflowStep.ZONE)
        return replace(self, zone=zone, step=WorkflowStep.LESION)

    def select_lesion(self, lesion: LesionCode) -> "HMIWorkflow":
        self._require_step(WorkflowStep.LESION)
        return replace(self, lesion=lesion, step=WorkflowStep.TREATMENT)

    def _require_step(self, expected: WorkflowStep) -> None:
        if self.step is not expected:
            raise ValueError(f"workflow step {self.step.value} does not allow {expected.value} selection")
