from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

from hoofcare.domain.jobs import Job, JobState


def _optional_id(name: str, value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be non-empty text")
    return value.strip()


@dataclass(frozen=True)
class StatisticsFilter:
    date_from: date
    date_to: date
    operator_id: str | None = None
    farm_id: str | None = None
    state: JobState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.date_from, date) or not isinstance(self.date_to, date):
            raise ValueError("date range values must be dates")
        if self.date_from > self.date_to:
            raise ValueError("date range must be ascending")
        object.__setattr__(self, "operator_id", _optional_id("operator_id", self.operator_id))
        object.__setattr__(self, "farm_id", _optional_id("farm_id", self.farm_id))
        if self.state is not None and not isinstance(self.state, JobState):
            raise ValueError("state must be a JobState")


@dataclass(frozen=True)
class MaterialQuantity:
    code: str
    unit: str
    quantity_scale: int
    quantity: Decimal


@dataclass(frozen=True)
class JobStatistics:
    completed_cows: int
    additional_material_quantities: tuple[MaterialQuantity, ...]
    open_jobs: int
    closed_jobs: int
    total_net_grosz: int


def derive_job_statistics(jobs: Iterable[Job], filter: StatisticsFilter) -> JobStatistics:
    if not isinstance(filter, StatisticsFilter):
        raise ValueError("filter must be a StatisticsFilter")
    selected: list[Job] = []
    for job in jobs:
        if not isinstance(job, Job):
            raise ValueError("statistics input must contain Job values")
        opened_date = job.opened_at.date()
        if not filter.date_from <= opened_date <= filter.date_to:
            continue
        if filter.operator_id is not None and job.operator_id != filter.operator_id:
            continue
        if filter.farm_id is not None and job.farm_id != filter.farm_id:
            continue
        if filter.state is not None and job.state is not filter.state:
            continue
        selected.append(job)

    metadata: dict[str, tuple[str, int]] = {}
    quantities: dict[str, Decimal] = {}
    for job in selected:
        for usage in job.usages:
            rate = job.pricing.rate(usage.material_code)
            identity = (rate.unit, rate.quantity_scale)
            previous = metadata.setdefault(rate.code, identity)
            if previous != identity:
                raise ValueError("material metadata conflict")
            quantities[rate.code] = quantities.get(rate.code, Decimal("0")) + usage.quantity

    material_quantities = tuple(
        MaterialQuantity(code, metadata[code][0], metadata[code][1], quantity)
        for code, quantity in sorted(quantities.items())
    )
    return JobStatistics(
        completed_cows=sum(job.completed_cows for job in selected),
        additional_material_quantities=material_quantities,
        open_jobs=sum(job.state is JobState.OPEN for job in selected),
        closed_jobs=sum(job.state is JobState.CLOSED for job in selected),
        total_net_grosz=sum(
            job.settlement().total_net_grosz
            for job in selected
            if job.state is JobState.CLOSED
        ),
    )
