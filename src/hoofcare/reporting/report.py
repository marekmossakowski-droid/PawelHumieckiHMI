from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from hoofcare.domain.clinical import CanonicalClinicalRecord
from hoofcare.reporting.pdf import render_minimal_pdf


class ReportAudience(str, Enum):
    FARMER = "FARMER"
    VETERINARIAN = "VETERINARIAN"
    ZOOTECHNICIAN = "ZOOTECHNICIAN"
    NUTRITIONIST = "NUTRITIONIST"
    TECHNICAL_SERVICE = "TECHNICAL_SERVICE"


@dataclass(frozen=True)
class ReportInput:
    report_id: str
    generated_at: datetime
    session_id: str
    animal_id: str
    lesion_summary: str
    treatment_summary: str
    material_summary: str
    media_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReportDocument:
    report_id: str
    source_session_id: str
    generated_at_iso: str
    animal_id: str
    sections: dict[ReportAudience, str]
    clinical_disclaimer: str
    synthetic_test_only: bool
    media_refs: tuple[str, ...]

    def to_pdf_bytes(self) -> bytes:
        lines = [
            f"Report-ID: {self.report_id}",
            f"Source-Session-ID: {self.source_session_id}",
            f"Generated-At: {self.generated_at_iso}",
            f"Animal-ID: {self.animal_id}",
            "Synthetic-Test-Only: true",
            f"Clinical-Disclaimer: {self.clinical_disclaimer}",
        ]
        for audience, text in self.sections.items():
            lines.append(f"[{audience.value}] {text}")
        for media_ref in self.media_refs:
            lines.append(f"Media-Ref: {media_ref}")
        return render_minimal_pdf(tuple(lines))


def _build_document(*, report_id: str, generated_at: datetime, session_id: str, animal_id: str, lesion_summary: str, treatment_summary: str, material_summary: str, media_refs: tuple[str, ...]) -> ReportDocument:
    common = (
        f"Animal {animal_id}; lesion: {lesion_summary}; "
        f"treatment: {treatment_summary}; materials: {material_summary}."
    )
    sections = {
        ReportAudience.FARMER: f"Treatment summary for herd follow-up. {common}",
        ReportAudience.VETERINARIAN: f"Clinical documentation for professional review. {common}",
        ReportAudience.ZOOTECHNICIAN: f"Animal-care and recurrence tracking summary. {common}",
        ReportAudience.NUTRITIONIST: f"Locomotion/hoof event context for nutrition review. {common}",
        ReportAudience.TECHNICAL_SERVICE: f"System/session provenance and treatment-record context. {common}",
    }
    return ReportDocument(
        report_id=report_id,
        source_session_id=session_id,
        generated_at_iso=generated_at.isoformat(),
        animal_id=animal_id,
        sections=sections,
        clinical_disclaimer=(
            "This system supports treatment documentation and does not replace veterinary examination or diagnosis."
        ),
        synthetic_test_only=True,
        media_refs=media_refs,
    )


def build_report_document(source: ReportInput, *, committed: bool = True) -> ReportDocument:
    if not committed:
        raise ValueError("report requires a committed canonical record")
    for name, value in {"report_id": source.report_id, "session_id": source.session_id, "animal_id": source.animal_id}.items():
        if not value.strip():
            raise ValueError(f"{name} must be non-empty")
    return _build_document(
        report_id=source.report_id,
        generated_at=source.generated_at,
        session_id=source.session_id,
        animal_id=source.animal_id,
        lesion_summary=source.lesion_summary,
        treatment_summary=source.treatment_summary,
        material_summary=source.material_summary,
        media_refs=tuple(source.media_refs),
    )


def build_report_from_canonical_record(
    record: CanonicalClinicalRecord,
    *,
    report_id: str,
    generated_at: datetime,
) -> ReportDocument:
    if not record.committed:
        raise ValueError("report requires a committed canonical record")
    if not report_id.strip():
        raise ValueError("report_id must be non-empty")
    if generated_at.tzinfo is None:
        raise ValueError("generated_at must be timezone-aware")

    lesion_summary = f"{record.lesion.label} [{record.lesion.code}] at {record.lesion.anatomical_zone}"
    treatment_summary = ", ".join(f"{item.label} [{item.code}]" for item in record.treatments)
    material_summary = ", ".join(
        f"{item.label} [{item.code}] {item.quantity:g} {item.unit}" for item in record.materials
    )
    media_refs = tuple(item.ref for item in record.media)

    return _build_document(
        report_id=report_id,
        generated_at=generated_at,
        session_id=record.session_id,
        animal_id=record.animal_id,
        lesion_summary=lesion_summary,
        treatment_summary=treatment_summary,
        material_summary=material_summary,
        media_refs=media_refs,
    )
