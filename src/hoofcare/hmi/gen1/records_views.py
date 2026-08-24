from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from hoofcare.application.job_statistics import (
    JobStatistics,
    MaterialQuantity,
    StatisticsFilter,
)
from hoofcare.domain.jobs import Job, JobState, SettlementLine
from hoofcare.hmi.gen1.shell import OwnerSession
from hoofcare.reporting.settlement import SettlementDocument, format_pln


_CAPABILITY_ACTIONS = {
    "farms.read": "open_farms",
    "materials.read": "open_materials",
    "operators.read": "open_operators",
    "history.read": "open_history",
    "reports.generate": "generate_report",
    "audit.read": "open_audit",
    "diagnostics.read": "open_diagnostics",
}


@dataclass(frozen=True)
class WorkStatisticsView:
    completed_cows: int
    material_quantities: tuple[MaterialQuantity, ...]
    open_jobs: int
    closed_jobs: int
    prices_visible: bool
    money_bindings: tuple[str, ...]
    primary_actions: tuple[str, ...]


@dataclass(frozen=True)
class HistoryItemView:
    job_id: str
    farm_id: str
    operator_id: str
    opened_at_iso: str
    state: JobState
    completed_cows: int
    settlement_available: bool


@dataclass(frozen=True)
class HistoryView:
    items: tuple[HistoryItemView, ...]
    filter: StatisticsFilter
    local_only: bool
    primary_actions: tuple[str, ...]


@dataclass(frozen=True)
class SettlementView:
    job_id: str
    lines: tuple[SettlementLine, ...]
    total_label: str
    disclaimer: str
    prices_visible: bool
    primary_actions: tuple[str, ...]


@dataclass(frozen=True)
class AdminCapabilityView:
    capability_ids: tuple[str, ...]
    visible_actions: tuple[str, ...]


@dataclass(frozen=True)
class OwnerDashboardView:
    surfaces: tuple[str, ...]
    synthetic_gate: bool
    primary_actions: tuple[str, ...]


def project_work_statistics(statistics: JobStatistics) -> WorkStatisticsView:
    if not isinstance(statistics, JobStatistics):
        raise ValueError("statistics must be JobStatistics")
    if any(
        value < 0
        for value in (
            statistics.completed_cows,
            statistics.open_jobs,
            statistics.closed_jobs,
        )
    ):
        raise ValueError("statistics counters cannot be negative")
    return WorkStatisticsView(
        completed_cows=statistics.completed_cows,
        material_quantities=statistics.additional_material_quantities,
        open_jobs=statistics.open_jobs,
        closed_jobs=statistics.closed_jobs,
        prices_visible=False,
        money_bindings=(),
        primary_actions=("open_history", "back"),
    )


def _matches(job: Job, filter: StatisticsFilter) -> bool:
    opened_date = job.opened_at.date()
    return (
        filter.date_from <= opened_date <= filter.date_to
        and (filter.operator_id is None or job.operator_id == filter.operator_id)
        and (filter.farm_id is None or job.farm_id == filter.farm_id)
        and (filter.state is None or job.state is filter.state)
    )


def project_history(
    jobs: tuple[Job, ...],
    filter: StatisticsFilter,
) -> HistoryView:
    if not isinstance(jobs, tuple):
        raise ValueError("jobs must be an immutable tuple")
    if any(not isinstance(job, Job) for job in jobs):
        raise ValueError("jobs must contain Job values")
    if not isinstance(filter, StatisticsFilter):
        raise ValueError("filter must be a StatisticsFilter")
    items = tuple(
        HistoryItemView(
            job_id=job.job_id,
            farm_id=job.farm_id,
            operator_id=job.operator_id,
            opened_at_iso=job.opened_at.isoformat(),
            state=job.state,
            completed_cows=job.completed_cows,
            settlement_available=job.state is JobState.CLOSED,
        )
        for job in jobs
        if _matches(job, filter)
    )
    settlement_actions = (
        ("open_settlement", "generate_pdf")
        if any(item.settlement_available for item in items)
        else ()
    )
    return HistoryView(
        items=items,
        filter=filter,
        local_only=True,
        primary_actions=settlement_actions + ("back",),
    )


def _require_consistent_document(document: SettlementDocument) -> None:
    if not isinstance(document, SettlementDocument):
        raise ValueError("document must be a SettlementDocument")
    if (
        type(document.total_net_grosz) is not int
        or document.total_net_grosz < 0
        or sum(line.total_net_grosz for line in document.lines)
        != document.total_net_grosz
    ):
        raise ValueError("settlement total is inconsistent")


def project_settlement(document: SettlementDocument) -> SettlementView:
    _require_consistent_document(document)
    return SettlementView(
        job_id=document.job_id,
        lines=document.lines,
        total_label=f"RAZEM NETTO: {format_pln(document.total_net_grosz)}",
        disclaimer=document.disclaimer,
        prices_visible=True,
        primary_actions=("generate_pdf", "open_history", "back"),
    )


def render_settlement_pdf(document: SettlementDocument) -> bytes:
    _require_consistent_document(document)
    return document.render_pdf()


def project_admin_capabilities(
    capability_ids: tuple[str, ...],
) -> AdminCapabilityView:
    if not isinstance(capability_ids, tuple):
        raise ValueError("capability_ids must be an immutable tuple")
    if any(not isinstance(item, str) or not item.strip() for item in capability_ids):
        raise ValueError("capability IDs must be non-empty text")
    allowed = tuple(
        capability
        for capability in dict.fromkeys(capability_ids)
        if capability in _CAPABILITY_ACTIONS
    )
    return AdminCapabilityView(
        capability_ids=allowed,
        visible_actions=tuple(_CAPABILITY_ACTIONS[item] for item in allowed),
    )


def project_owner_dashboard(
    owner_session: OwnerSession,
    now: datetime,
    capability_ids: tuple[str, ...],
) -> OwnerDashboardView:
    if not isinstance(owner_session, OwnerSession) or not owner_session.is_active(now):
        raise ValueError("active owner session is required")
    capabilities = project_admin_capabilities(capability_ids)
    return OwnerDashboardView(
        surfaces=capabilities.visible_actions,
        synthetic_gate=True,
        primary_actions=("back",),
    )
