from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from hoofcare.domain.jobs import Job, JobState


class JobScreenStage(str, Enum):
    OPEN = "OPEN"
    PRICE_CORRECTION = "PRICE_CORRECTION"
    TREATMENT = "TREATMENT"
    SUMMARY = "SUMMARY"


@dataclass(frozen=True)
class JobMenuView:
    prices_visible: bool
    price_edit_allowed: bool
    cow_count: int
    material_quantities: tuple[tuple[str, Decimal], ...]
    actions: tuple[str, ...]


def job_menu_view(job: Job, stage: JobScreenStage) -> JobMenuView:
    if not isinstance(job, Job):
        raise ValueError("job must be a Job")
    if not isinstance(stage, JobScreenStage):
        raise ValueError("stage must be a JobScreenStage")

    quantities: dict[str, Decimal] = {}
    for usage in job.usages:
        quantities[usage.material_code] = (
            quantities.get(usage.material_code, Decimal("0")) + usage.quantity
        )

    prices_visible = stage in {
        JobScreenStage.OPEN,
        JobScreenStage.PRICE_CORRECTION,
        JobScreenStage.SUMMARY,
    }
    price_edit_allowed = (
        job.state is JobState.OPEN
        and not job.pricing_frozen
        and stage in {
            JobScreenStage.OPEN,
            JobScreenStage.PRICE_CORRECTION,
            JobScreenStage.SUMMARY,
        }
    )

    if stage is JobScreenStage.OPEN:
        actions = ("set_prices", "open_job")
    elif stage is JobScreenStage.PRICE_CORRECTION:
        actions = ("correct_price", "back") if price_edit_allowed else ("back",)
    elif stage is JobScreenStage.TREATMENT:
        actions = ("record_treatment", "add_material", "complete_cow")
    else:
        actions = ("close_job",)
        if price_edit_allowed:
            actions = ("correct_price",) + actions

    return JobMenuView(
        prices_visible=prices_visible,
        price_edit_allowed=price_edit_allowed,
        cow_count=job.completed_cows,
        material_quantities=tuple(sorted(quantities.items())),
        actions=actions,
    )
