from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

from hoofcare.application.job_service import JobService
from hoofcare.application.job_statistics import StatisticsFilter, derive_job_statistics
from hoofcare.domain.jobs import Job, JobPricingSnapshot, MaterialRate
from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionState
from hoofcare.hmi.job_menu import closed_job_summary_view, daily_work_view
from hoofcare.persistence.job_store import LocalJobStore
from hoofcare.persistence.local_store import LocalSessionStore
from hoofcare.reporting.settlement import SettlementDocument


@dataclass(frozen=True)
class SettlementScenarioResult:
    completed_cows: int
    block_quantity: str
    total_net_grosz: int
    work_prices_visible: bool
    total_label: str
    restart_consistent: bool
    pdf_bytes: bytes


class SyntheticJobSettlementScenario:
    """Exercise the bounded S1 workflow through durable local boundaries."""

    JOB_ID = "SYNTHETIC-JOB-S1"
    OPENED_AT = datetime(2026, 8, 23, 8, tzinfo=timezone.utc)
    CLOSED_AT = datetime(2026, 8, 23, 18, tzinfo=timezone.utc)
    GENERATED_AT = datetime(2026, 8, 23, 19, tzinfo=timezone.utc)

    def __init__(self, root: Path) -> None:
        if not isinstance(root, Path):
            raise ValueError("root must be a Path")
        self.root = root

    def run(self) -> SettlementScenarioResult:
        jobs = LocalJobStore(self.root / "jobs")
        sessions = LocalSessionStore(self.root / "sessions")
        jobs.save(self._open_job())
        service = JobService(jobs, sessions)

        for index in (1, 2):
            session = self._completed_session(index)
            service.commit_completed_session(
                self.JOB_ID,
                session,
                f"SYNTHETIC-COMPLETE-{index}",
            )

        # An identical durable retry must not increment the derived cow count.
        service.commit_completed_session(
            self.JOB_ID,
            self._completed_session(2),
            "SYNTHETIC-COMPLETE-2",
        )

        for index in (1, 2):
            current = jobs.load(self.JOB_ID)
            updated = current.record_material(
                f"SYNTHETIC-BLOCK-{index}",
                f"SYNTHETIC-SESSION-{index}",
                "BLOCK",
                Decimal("1"),
            )
            jobs.save(updated)

        restarted_jobs = LocalJobStore(jobs.root)
        restarted_sessions = LocalSessionStore(sessions.root)
        restarted_service = JobService(restarted_jobs, restarted_sessions)
        durable = restarted_jobs.load(self.JOB_ID)
        durable_session_ids = tuple(
            restarted_sessions.load(session_id).session_id
            for session_id in durable.completed_session_ids
        )
        if restarted_service.reconciliation_required(
            self.JOB_ID, durable_session_ids
        ):
            raise ValueError("synthetic completed sessions require reconciliation")

        closed = durable.close(self.CLOSED_AT, ())
        restarted_jobs.save(closed)

        final_jobs = LocalJobStore(restarted_jobs.root)
        final_job = final_jobs.load(self.JOB_ID)
        statistics = derive_job_statistics(
            final_jobs.list_jobs(),
            StatisticsFilter(
                date_from=date(2026, 8, 23),
                date_to=date(2026, 8, 23),
                operator_id="SYNTHETIC-PAWEL",
                farm_id="SYNTHETIC-FARM",
            ),
        )
        work_view = daily_work_view(statistics)
        document = SettlementDocument.from_closed_job(final_job, self.GENERATED_AT)
        summary_view = closed_job_summary_view(document)
        pdf_bytes = document.render_pdf()

        verification_store = LocalJobStore(final_jobs.root)
        verification_job = verification_store.load(self.JOB_ID)
        verification_statistics = derive_job_statistics(
            verification_store.list_jobs(),
            StatisticsFilter(date(2026, 8, 23), date(2026, 8, 23)),
        )
        verification_document = SettlementDocument.from_closed_job(
            verification_job, self.GENERATED_AT
        )
        restart_consistent = (
            verification_statistics == statistics
            and verification_document == document
            and verification_document.render_pdf() == pdf_bytes
        )

        block_quantity = next(
            item.quantity
            for item in statistics.additional_material_quantities
            if item.code == "BLOCK"
        )
        return SettlementScenarioResult(
            completed_cows=work_view.completed_cows,
            block_quantity=format(block_quantity, "f"),
            total_net_grosz=summary_view.total_net_grosz,
            work_prices_visible=work_view.prices_visible,
            total_label=summary_view.total_label,
            restart_consistent=restart_consistent,
            pdf_bytes=pdf_bytes,
        )

    def _open_job(self) -> Job:
        pricing = JobPricingSnapshot(
            cow_unit_price_grosz=3500,
            additional_materials=(
                MaterialRate("BLOCK", "Klocek", "szt.", 2600, 0),
            ),
        )
        return Job.open(
            self.JOB_ID,
            "SYNTHETIC-FARM",
            "SYNTHETIC-PAWEL",
            self.OPENED_AT,
            pricing,
            planned_cows=2,
        )

    @staticmethod
    def _completed_session(index: int) -> Session:
        animal_id = f"SYNTHETIC-COW-{index}"
        session_id = f"SYNTHETIC-SESSION-{index}"
        return Session(
            session_id=session_id,
            state=SessionState.COMPLETED,
            identity=AnimalIdentityResolution.confirmed(animal_id),
            animal_id=animal_id,
            applied_event_ids=(
                f"SYNTHETIC-IDENTITY-{index}",
                f"SYNTHETIC-SESSION-COMPLETE-{index}",
            ),
        )
