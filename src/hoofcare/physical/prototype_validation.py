from __future__ import annotations

from datetime import datetime
from pathlib import Path

from hoofcare.domain.session import Session
from hoofcare.persistence.local_store import LocalSessionStore
from hoofcare.reporting.report import ReportInput, build_report_document


class PhysicalPrototypeValidator:
    """Isolated synthetic/test-only persistence and reporting validation seam."""

    kvk_connection_allowed = False
    real_farm_data_allowed = False

    def __init__(self, root: Path) -> None:
        self._store = LocalSessionStore(Path(root))

    def commit_session(self, session: Session) -> None:
        self._store.save(session)

    def recover_session(self, session_id: str) -> Session:
        return self._store.load(session_id)

    def generate_report(
        self,
        session_id: str,
        *,
        report_id: str,
        generated_at: datetime,
        lesion_summary: str,
        treatment_summary: str,
        material_summary: str,
    ) -> bytes:
        session = self._store.load(session_id)
        if not session.animal_id:
            raise ValueError("committed session must have a resolved animal identity")
        document = build_report_document(
            ReportInput(
                report_id=report_id,
                generated_at=generated_at,
                session_id=session.session_id,
                animal_id=session.animal_id,
                lesion_summary=lesion_summary,
                treatment_summary=treatment_summary,
                material_summary=material_summary,
                media_refs=session.media_refs,
            ),
            committed=True,
        )
        return document.to_pdf_bytes()
