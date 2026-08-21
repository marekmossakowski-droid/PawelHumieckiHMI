from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
        # Bench-only deterministic minimal PDF-like document. This deliberately
        # avoids external dependencies and network/cloud output.
        lines = [
            "%PDF-1.4",
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
        lines.append("%%EOF")
        return ("\n".join(lines) + "\n").encode("utf-8")


def build_report_document(source: ReportInput, *, committed: bool = True) -> ReportDocument:
    if not committed:
        raise ValueError("report requires a committed canonical record")

    for name, value in {
        "report_id": source.report_id,
        "session_id": source.session_id,
        "animal_id": source.animal_id,
    }.items():
        if not value.strip():
            raise ValueError(f"{name} must be non-empty")

    common = (
        f"Animal {source.animal_id}; lesion: {source.lesion_summary}; "
        f"treatment: {source.treatment_summary}; materials: {source.material_summary}."
    )
    sections = {
        ReportAudience.FARMER: f"Treatment summary for herd follow-up. {common}",
        ReportAudience.VETERINARIAN: f"Clinical documentation for professional review. {common}",
        ReportAudience.ZOOTECHNICIAN: f"Animal-care and recurrence tracking summary. {common}",
        ReportAudience.NUTRITIONIST: f"Locomotion/hoof event context for nutrition review. {common}",
        ReportAudience.TECHNICAL_SERVICE: f"System/session provenance and treatment-record context. {common}",
    }

    return ReportDocument(
        report_id=source.report_id,
        source_session_id=source.session_id,
        generated_at_iso=source.generated_at.isoformat(),
        animal_id=source.animal_id,
        sections=sections,
        clinical_disclaimer=(
            "This system supports treatment documentation and does not replace veterinary examination or diagnosis."
        ),
        synthetic_test_only=True,
        media_refs=tuple(source.media_refs),
    )
