from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from hoofcare.application.job_statistics import JobStatistics, MaterialQuantity
from hoofcare.domain.jobs import Job, JobState
from hoofcare.domain.jobs import SettlementLine
from hoofcare.reporting.settlement import SettlementDocument, format_pln


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


@dataclass(frozen=True)
class DailyWorkView:
    completed_cows: int
    material_quantities: tuple[MaterialQuantity, ...]
    open_jobs: int
    closed_jobs: int
    prices_visible: bool
    data_bindings: tuple[str, ...]


@dataclass(frozen=True)
class ClosedJobSummaryView:
    settlement_id: str
    lines: tuple[SettlementLine, ...]
    total_net_grosz: int
    total_label: str
    prices_visible: bool
    actions: tuple[str, ...]


def daily_work_view(statistics: JobStatistics) -> DailyWorkView:
    if not isinstance(statistics, JobStatistics):
        raise ValueError("statistics must be JobStatistics")
    return DailyWorkView(
        completed_cows=statistics.completed_cows,
        material_quantities=statistics.additional_material_quantities,
        open_jobs=statistics.open_jobs,
        closed_jobs=statistics.closed_jobs,
        prices_visible=False,
        data_bindings=(
            "completed_cows",
            "material_quantities",
            "open_jobs",
            "closed_jobs",
        ),
    )


def closed_job_summary_view(document: SettlementDocument) -> ClosedJobSummaryView:
    if not isinstance(document, SettlementDocument):
        raise ValueError("document must be SettlementDocument")
    return ClosedJobSummaryView(
        settlement_id=document.settlement_id,
        lines=document.lines,
        total_net_grosz=document.total_net_grosz,
        total_label=f"RAZEM NETTO: {format_pln(document.total_net_grosz)}",
        prices_visible=True,
        actions=("generate_settlement_pdf", "back_to_dashboard"),
    )


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
