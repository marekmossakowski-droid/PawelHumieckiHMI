from hoofcare.domain.jobs import Job
from hoofcare.domain.session import Session, SessionState
from hoofcare.persistence.job_store import LocalJobStore
from hoofcare.persistence.local_store import LocalSessionStore


class JobService:
    def __init__(self, jobs: LocalJobStore, sessions: LocalSessionStore) -> None:
        self.jobs = jobs
        self.sessions = sessions

    def commit_completed_session(
        self,
        job_id: str,
        session: Session,
        event_id: str,
    ) -> Job:
        if session.state is not SessionState.COMPLETED:
            raise ValueError("session must be completed before job counting")
        self.sessions.save(session)
        current = self.jobs.load(job_id)
        updated = current.record_completed_session(session, event_id)
        self.jobs.save(updated)
        return updated

    def reconciliation_required(
        self,
        job_id: str,
        durable_completed_session_ids: tuple[str, ...],
    ) -> tuple[str, ...]:
        if not isinstance(durable_completed_session_ids, tuple):
            raise ValueError("durable session identifiers must be an immutable tuple")
        job = self.jobs.load(job_id)
        durable = tuple(dict.fromkeys(durable_completed_session_ids))
        return tuple(
            session_id
            for session_id in durable
            if session_id not in job.completed_session_ids
        )
