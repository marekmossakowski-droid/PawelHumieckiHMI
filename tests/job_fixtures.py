from datetime import datetime, timezone
from decimal import Decimal

from hoofcare.domain.jobs import Job, JobPricingSnapshot, MaterialRate
from hoofcare.domain.session import AnimalIdentityResolution, Session, SessionState


OPENED = datetime(2026, 8, 23, 8, tzinfo=timezone.utc)
CLOSED = datetime(2026, 8, 23, 18, tzinfo=timezone.utc)


def completed_session(animal_id: str, session_id: str) -> Session:
    return Session(
        session_id=session_id,
        state=SessionState.COMPLETED,
        identity=AnimalIdentityResolution.confirmed(animal_id),
        animal_id=animal_id,
        applied_event_ids=(f"identity-{session_id}", f"complete-{session_id}"),
    )


def open_job_fixture() -> Job:
    pricing = JobPricingSnapshot(
        3500,
        (MaterialRate("BLOCK", "Klocek", "szt.", 2600, 0),),
    )
    return Job.open(
        "TEST-JOB-1",
        "TEST-FARM-1",
        "operator-pawel",
        OPENED,
        pricing,
        40,
    )


def closed_job_fixture() -> Job:
    job = open_job_fixture()
    for index in range(1, 41):
        session = completed_session(
            f"TEST-COW-{index:03d}",
            f"TEST-SESSION-{index:03d}",
        )
        job = job.record_completed_session(session, f"job-complete-{index}")
    for index, session_id in enumerate(job.completed_session_ids[:6], start=1):
        job = job.record_material(
            f"block-{index}",
            session_id,
            "BLOCK",
            Decimal("1"),
        )
    return job.close(CLOSED, ())


def closed_job(
    job_id: str,
    operator_id: str,
    cow_count: int,
    expected_total_grosz: int,
    farm_id: str = "TEST-FARM-1",
) -> Job:
    if cow_count <= 0 or expected_total_grosz % cow_count:
        raise ValueError("fixture total must divide exactly by positive cow_count")
    job = Job.open(
        job_id,
        farm_id,
        operator_id,
        OPENED,
        JobPricingSnapshot(expected_total_grosz // cow_count, ()),
        cow_count,
    )
    for index in range(1, cow_count + 1):
        session = completed_session(
            f"{job_id}-COW-{index}",
            f"{job_id}-SESSION-{index}",
        )
        job = job.record_completed_session(session, f"{job_id}-EVENT-{index}")
    closed = job.close(CLOSED, ())
    if closed.settlement().total_net_grosz != expected_total_grosz:
        raise AssertionError("synthetic fixture total mismatch")
    return closed
