from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

from hoofcare.domain.session import Session, SessionState


def _text(name: str, value: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be text")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must be non-empty")
    return normalized


@dataclass(frozen=True)
class MaterialRate:
    code: str
    label: str
    unit: str
    unit_price_grosz: int
    quantity_scale: int
    job_local: bool = False
    active: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _text("material code", self.code))
        object.__setattr__(self, "label", _text("material label", self.label))
        object.__setattr__(self, "unit", _text("material unit", self.unit))
        if type(self.unit_price_grosz) is not int or self.unit_price_grosz < 0:
            raise ValueError("unit price must be non-negative integer grosze")
        if type(self.quantity_scale) is not int or self.quantity_scale not in range(4):
            raise ValueError("quantity scale must be between zero and three")
        if type(self.job_local) is not bool:
            raise ValueError("job_local must be boolean")
        if type(self.active) is not bool:
            raise ValueError("active must be boolean")

    def normalize_quantity(self, quantity: Decimal) -> Decimal:
        if (
            not isinstance(quantity, Decimal)
            or not quantity.is_finite()
            or quantity <= 0
        ):
            raise ValueError("quantity must be a positive finite Decimal")
        quantum = Decimal(1).scaleb(-self.quantity_scale)
        normalized = quantity.quantize(quantum)
        if normalized != quantity:
            raise ValueError("quantity exceeds material precision")
        return normalized

    def line_total_grosz(self, quantity: Decimal) -> int:
        normalized = self.normalize_quantity(quantity)
        amount = normalized * Decimal(self.unit_price_grosz)
        return int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@dataclass(frozen=True)
class JobPricingSnapshot:
    cow_unit_price_grosz: int
    additional_materials: tuple[MaterialRate, ...]

    def __post_init__(self) -> None:
        if type(self.cow_unit_price_grosz) is not int or self.cow_unit_price_grosz < 0:
            raise ValueError("cow price must be non-negative integer grosze")
        if not isinstance(self.additional_materials, tuple):
            raise ValueError("additional materials must be an immutable tuple")
        if any(not isinstance(rate, MaterialRate) for rate in self.additional_materials):
            raise ValueError("additional materials must contain MaterialRate values")
        codes = tuple(rate.code for rate in self.additional_materials)
        if len(codes) != len(set(codes)):
            raise ValueError("material codes must be unique within job pricing")
        if any(not rate.active for rate in self.additional_materials):
            raise ValueError("job pricing accepts only active materials")

    def cow_subtotal_grosz(self, completed_cows: int) -> int:
        if type(completed_cows) is not int or completed_cows < 0:
            raise ValueError("completed cows must be a non-negative integer")
        return completed_cows * self.cow_unit_price_grosz

    def rate(self, code: str) -> MaterialRate:
        normalized_code = _text("material code", code)
        for item in self.additional_materials:
            if item.code == normalized_code:
                return item
        raise KeyError(normalized_code)

    def with_local_material(self, rate: MaterialRate) -> "JobPricingSnapshot":
        if not isinstance(rate, MaterialRate) or not rate.job_local or not rate.active:
            raise ValueError("job-local extension requires an active job_local material")
        return replace(
            self,
            additional_materials=self.additional_materials + (rate,),
        )


class JobState(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class CompletedSessionLink:
    event_id: str
    session_id: str
    animal_id: str


@dataclass(frozen=True)
class MaterialUsage:
    event_id: str
    session_id: str
    material_code: str
    quantity: Decimal


@dataclass(frozen=True)
class SettlementLine:
    code: str
    label: str
    quantity: Decimal
    unit: str
    unit_price_grosz: int
    total_net_grosz: int


@dataclass(frozen=True)
class Settlement:
    settlement_id: str
    job_id: str
    closed_at: datetime
    lines: tuple[SettlementLine, ...]
    total_net_grosz: int


@dataclass(frozen=True)
class Job:
    job_id: str
    farm_id: str
    operator_id: str
    opened_at: datetime
    pricing: JobPricingSnapshot
    planned_cows: int | None
    state: JobState = JobState.OPEN
    completed_links: tuple[CompletedSessionLink, ...] = ()
    usages: tuple[MaterialUsage, ...] = ()
    closed_settlement: Settlement | None = None

    @classmethod
    def open(
        cls,
        job_id: str,
        farm_id: str,
        operator_id: str,
        opened_at: datetime,
        pricing: JobPricingSnapshot,
        planned_cows: int | None,
    ) -> "Job":
        if opened_at.tzinfo is None:
            raise ValueError("opened_at must be timezone-aware")
        if planned_cows is not None and (
            type(planned_cows) is not int or planned_cows < 0
        ):
            raise ValueError("planned_cows must be a non-negative integer")
        if not isinstance(pricing, JobPricingSnapshot):
            raise ValueError("pricing must be a JobPricingSnapshot")
        return cls(
            _text("job_id", job_id),
            _text("farm_id", farm_id),
            _text("operator_id", operator_id),
            opened_at,
            pricing,
            planned_cows,
        )

    @property
    def completed_cows(self) -> int:
        return len(self.completed_links)

    @property
    def completed_session_ids(self) -> tuple[str, ...]:
        return tuple(link.session_id for link in self.completed_links)

    @property
    def animal_ids(self) -> tuple[str, ...]:
        return tuple(link.animal_id for link in self.completed_links)

    @property
    def material_total_grosz(self) -> int:
        return sum(
            self.pricing.rate(item.material_code).line_total_grosz(item.quantity)
            for item in self.usages
        )

    def record_completed_session(self, session: Session, event_id: str) -> "Job":
        self._require_open()
        if (
            not isinstance(session, Session)
            or session.state is not SessionState.COMPLETED
            or not session.animal_id
        ):
            raise ValueError("only completed identified sessions are billable")
        normalized_event_id = _text("event_id", event_id)
        for link in self.completed_links:
            if link.event_id == normalized_event_id:
                if (link.session_id, link.animal_id) == (
                    session.session_id,
                    session.animal_id,
                ):
                    return self
                raise ValueError("completion event payload conflict")
        if (
            session.session_id in self.completed_session_ids
            or session.animal_id in self.animal_ids
        ):
            raise ValueError("session or animal already counted in job")
        link = CompletedSessionLink(
            normalized_event_id,
            session.session_id,
            session.animal_id,
        )
        return replace(self, completed_links=self.completed_links + (link,))

    def record_material(
        self,
        event_id: str,
        session_id: str,
        material_code: str,
        quantity: Decimal,
    ) -> "Job":
        self._require_open()
        normalized_session_id = _text("session_id", session_id)
        if normalized_session_id not in self.completed_session_ids:
            raise ValueError("material requires a completed session linked to this job")
        rate = self.pricing.rate(material_code)
        normalized = rate.normalize_quantity(quantity)
        usage = MaterialUsage(
            _text("event_id", event_id),
            normalized_session_id,
            rate.code,
            normalized,
        )
        for existing in self.usages:
            if existing.event_id == usage.event_id:
                if existing == usage:
                    return self
                raise ValueError("material event payload conflict")
        return replace(self, usages=self.usages + (usage,))

    def add_local_material(self, rate: MaterialRate) -> "Job":
        self._require_open()
        return replace(self, pricing=self.pricing.with_local_material(rate))

    def close(
        self,
        closed_at: datetime,
        unresolved_session_ids: tuple[str, ...],
    ) -> "Job":
        self._require_open()
        if not isinstance(closed_at, datetime) or closed_at.tzinfo is None:
            raise ValueError("closed_at must be timezone-aware")
        if not isinstance(unresolved_session_ids, tuple):
            raise ValueError("unresolved_session_ids must be an immutable tuple")
        if unresolved_session_ids:
            raise ValueError("job closure requires no unresolved sessions")
        settlement = self._build_settlement(closed_at)
        return replace(
            self,
            state=JobState.CLOSED,
            closed_settlement=settlement,
        )

    def settlement(self) -> Settlement:
        if self.closed_settlement is None:
            raise ValueError("job is not closed")
        return self.closed_settlement

    def _require_open(self) -> None:
        if self.state is not JobState.OPEN:
            raise ValueError("job must be open")

    def _build_settlement(self, closed_at: datetime) -> Settlement:
        cow_line = SettlementLine(
            "COW",
            "Wykonane krowy",
            Decimal(self.completed_cows),
            "szt.",
            self.pricing.cow_unit_price_grosz,
            self.pricing.cow_subtotal_grosz(self.completed_cows),
        )
        quantities: dict[str, Decimal] = {}
        for usage in self.usages:
            quantities[usage.material_code] = (
                quantities.get(usage.material_code, Decimal("0")) + usage.quantity
            )
        material_lines = tuple(
            SettlementLine(
                code,
                self.pricing.rate(code).label,
                quantity,
                self.pricing.rate(code).unit,
                self.pricing.rate(code).unit_price_grosz,
                self.pricing.rate(code).line_total_grosz(quantity),
            )
            for code, quantity in sorted(quantities.items())
        )
        lines = (cow_line,) + material_lines
        return Settlement(
            f"{self.job_id}-SETTLEMENT-1",
            self.job_id,
            closed_at,
            lines,
            sum(line.total_net_grosz for line in lines),
        )
