from __future__ import annotations

from dataclasses import dataclass

from hoofcare.application.job_statistics import JobStatistics, MaterialQuantity
from hoofcare.domain.jobs import Job, JobPricingSnapshot, JobState
from hoofcare.hmi.job_menu import JobScreenStage, job_menu_view


@dataclass(frozen=True)
class JobOpeningView:
    job_id: str
    farm_id: str
    operator_id: str
    planned_cows: int | None
    pricing: JobPricingSnapshot
    pricing_version: int
    prices_visible: bool
    price_edit_allowed: bool
    actions: tuple[str, ...]


@dataclass(frozen=True)
class ActiveJobView:
    job_id: str
    farm_id: str
    completed_cows: int
    planned_cows: int | None
    unfinished_sessions: int
    material_quantities: tuple[MaterialQuantity, ...]
    prices_visible: bool
    primary_actions: tuple[str, ...]


def _require_job(job: Job) -> None:
    if not isinstance(job, Job):
        raise ValueError("job must be a Job")


def project_job_opening(job: Job) -> JobOpeningView:
    _require_job(job)
    menu = job_menu_view(job, JobScreenStage.OPEN)
    return JobOpeningView(
        job_id=job.job_id,
        farm_id=job.farm_id,
        operator_id=job.operator_id,
        planned_cows=job.planned_cows,
        pricing=job.pricing,
        pricing_version=job.pricing_version,
        prices_visible=menu.prices_visible,
        price_edit_allowed=menu.price_edit_allowed,
        actions=menu.actions,
    )


def project_active_job(job: Job, statistics: JobStatistics) -> ActiveJobView:
    _require_job(job)
    if not isinstance(statistics, JobStatistics):
        raise ValueError("statistics must be JobStatistics")
    if job.state is not JobState.OPEN:
        raise ValueError("active job must be open")
    menu = job_menu_view(job, JobScreenStage.ACTIVE_WORK)
    statistic_quantities = tuple(
        (item.code, item.quantity)
        for item in statistics.additional_material_quantities
    )
    if (
        statistics.completed_cows != job.completed_cows
        or statistics.open_jobs != 1
        or statistics.closed_jobs != 0
        or statistics.total_net_grosz != 0
        or statistic_quantities != menu.material_quantities
    ):
        raise ValueError("statistics do not match job")

    return ActiveJobView(
        job_id=job.job_id,
        farm_id=job.farm_id,
        completed_cows=statistics.completed_cows,
        planned_cows=job.planned_cows,
        unfinished_sessions=0,
        material_quantities=statistics.additional_material_quantities,
        prices_visible=menu.prices_visible,
        primary_actions=menu.actions,
    )
