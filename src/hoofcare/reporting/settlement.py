from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from hoofcare.domain.jobs import Job, JobState, SettlementLine
from hoofcare.reporting.pdf import render_minimal_pdf


def format_pln(grosz: int) -> str:
    if type(grosz) is not int or grosz < 0:
        raise ValueError("amount must be non-negative integer grosz")
    whole, remainder = divmod(grosz, 100)
    return f"{whole:,}".replace(",", " ") + f",{remainder:02d} zł"


@dataclass(frozen=True)
class SettlementDocument:
    settlement_id: str
    job_id: str
    farm_id: str
    operator_id: str
    generated_at_iso: str
    lines: tuple[SettlementLine, ...]
    total_net_grosz: int
    disclaimer: str = "DOKUMENT ROZLICZENIOWY — NIE JEST FAKTURĄ"

    @classmethod
    def from_closed_job(cls, job: Job, generated_at: datetime) -> "SettlementDocument":
        if not isinstance(job, Job) or job.state is not JobState.CLOSED:
            raise ValueError("settlement document requires a closed job")
        if not isinstance(generated_at, datetime) or generated_at.tzinfo is None:
            raise ValueError("generated_at must be timezone-aware")
        settlement = job.settlement()
        if sum(line.total_net_grosz for line in settlement.lines) != settlement.total_net_grosz:
            raise ValueError("stored settlement total is inconsistent")
        return cls(
            settlement.settlement_id,
            job.job_id,
            job.farm_id,
            job.operator_id,
            generated_at.isoformat(),
            settlement.lines,
            settlement.total_net_grosz,
        )

    def render_pdf(self) -> bytes:
        lines = [
            "DOKUMENT ROZLICZENIOWY - NIE JEST FAKTURA",
            f"Settlement-ID: {self.settlement_id}",
            f"Job-ID: {self.job_id}",
            f"Farm-ID: {self.farm_id}",
            f"Operator-ID: {self.operator_id}",
            f"Generated-At: {self.generated_at_iso}",
        ]
        for line in self.lines:
            unit_price = format_pln(line.unit_price_grosz).replace("zł", "zl")
            line_total = format_pln(line.total_net_grosz).replace("zł", "zl")
            lines.append(
                f"{line.code} | {line.label} | {format(line.quantity, 'f')} {line.unit} | "
                f"{unit_price} | {line_total}"
            )
        total = format_pln(self.total_net_grosz).replace("zł", "zl")
        lines.append(f"RAZEM NETTO: {total}")
        return render_minimal_pdf(tuple(lines))

