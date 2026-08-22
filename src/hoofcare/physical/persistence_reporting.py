from __future__ import annotations

from datetime import datetime
from pathlib import Path

from hoofcare.domain.session import Session, SessionEvent, SessionEventType
from hoofcare.persistence.local_store import LocalSessionStore
from hoofcare.reporting.report import ReportDocument, ReportInput, build_report_document


class PhysicalPersistenceReportingValidator:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.store = LocalSessionStore(self.root / "sessions")
        self.synthetic_test_only = True
        self.kvk_connection_allowed = False
        self.real_farm_data_allowed = False

    def commit_session(self, session: Session) -> None:
        self.store.save(session)

    def complete_and_commit(self, session: Session, *, event_id: str) -> Session:
        completed = session.apply(SessionEvent(event_id=event_id, event_type=SessionEventType.COMPLETE))
        self.store.save(completed)
        return completed

    def recover_session(self, session_id: str) -> Session:
        return self.store.load(session_id)

    def build_local_report(
        self,
        session_id: str,
        *,
        report_id: str,
        generated_at: datetime,
        lesion_summary: str,
        treatment_summary: str,
        material_summary: str,
    ) -> ReportDocument:
        session = self.store.load(session_id)
        if not session.animal_id:
            raise ValueError("committed session must have confirmed animal identity")

        source = ReportInput(
            report_id=report_id,
            generated_at=generated_at,
            session_id=session.session_id,
            animal_id=session.animal_id,
            lesion_summary=lesion_summary,
            treatment_summary=treatment_summary,
            material_summary=material_summary,
            media_refs=tuple(session.media_refs),
        )
        return build_report_document(source, committed=True)
