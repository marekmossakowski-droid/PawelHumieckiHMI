from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from hoofcare.domain.jobs import (
    CompletedSessionLink,
    Job,
    JobPricingSnapshot,
    JobState,
    MaterialRate,
    MaterialUsage,
    PriceCorrection,
    PriceField,
    Settlement,
    SettlementLine,
)


def _digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _safe_id(value: str) -> str:
    if not isinstance(value, str) or not value or value in {".", ".."}:
        raise ValueError("invalid job_id")
    if "/" in value or "\\" in value or Path(value).name != value:
        raise ValueError("invalid job_id")
    return value


def _aware_datetime(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("datetime must be text")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return parsed


def _material_rate(payload: dict[str, Any]) -> MaterialRate:
    return MaterialRate(
        code=payload["code"],
        label=payload["label"],
        unit=payload["unit"],
        unit_price_grosz=payload["unit_price_grosz"],
        quantity_scale=payload["quantity_scale"],
        job_local=payload["job_local"],
        active=payload["active"],
    )


def _serialize_job(job: Job) -> dict[str, Any]:
    settlement = job.closed_settlement
    return {
        "job_id": job.job_id,
        "farm_id": job.farm_id,
        "operator_id": job.operator_id,
        "opened_at": job.opened_at.isoformat(),
        "planned_cows": job.planned_cows,
        "state": job.state.value,
        "pricing_version": job.pricing_version,
        "price_corrections": [
            {
                "event_id": correction.event_id,
                "operator_id": correction.operator_id,
                "corrected_at": correction.corrected_at.isoformat(),
                "reason": correction.reason,
                "field": correction.field.value,
                "material_code": correction.material_code,
                "old_value_grosz": correction.old_value_grosz,
                "new_value_grosz": correction.new_value_grosz,
            }
            for correction in job.price_corrections
        ],
        "pricing": {
            "cow_unit_price_grosz": job.pricing.cow_unit_price_grosz,
            "additional_materials": [
                {
                    "code": rate.code,
                    "label": rate.label,
                    "unit": rate.unit,
                    "unit_price_grosz": rate.unit_price_grosz,
                    "quantity_scale": rate.quantity_scale,
                    "job_local": rate.job_local,
                    "active": rate.active,
                }
                for rate in job.pricing.additional_materials
            ],
        },
        "completed_links": [
            {
                "event_id": link.event_id,
                "session_id": link.session_id,
                "animal_id": link.animal_id,
            }
            for link in job.completed_links
        ],
        "usages": [
            {
                "event_id": usage.event_id,
                "session_id": usage.session_id,
                "material_code": usage.material_code,
                "quantity": format(usage.quantity, "f"),
            }
            for usage in job.usages
        ],
        "closed_settlement": None
        if settlement is None
        else {
            "settlement_id": settlement.settlement_id,
            "job_id": settlement.job_id,
            "closed_at": settlement.closed_at.isoformat(),
            "lines": [
                {
                    "code": line.code,
                    "label": line.label,
                    "quantity": format(line.quantity, "f"),
                    "unit": line.unit,
                    "unit_price_grosz": line.unit_price_grosz,
                    "total_net_grosz": line.total_net_grosz,
                }
                for line in settlement.lines
            ],
            "total_net_grosz": settlement.total_net_grosz,
        },
    }


def _deserialize_job(payload: dict[str, Any]) -> Job:
    pricing_payload = payload["pricing"]
    pricing = JobPricingSnapshot(
        cow_unit_price_grosz=pricing_payload["cow_unit_price_grosz"],
        additional_materials=tuple(
            _material_rate(rate) for rate in pricing_payload["additional_materials"]
        ),
    )
    opened_at = _aware_datetime(payload["opened_at"])
    base = Job.open(
        payload["job_id"],
        payload["farm_id"],
        payload["operator_id"],
        opened_at,
        pricing,
        payload["planned_cows"],
    )
    links = tuple(
        CompletedSessionLink(
            event_id=item["event_id"],
            session_id=item["session_id"],
            animal_id=item["animal_id"],
        )
        for item in payload["completed_links"]
    )
    usages = tuple(
        MaterialUsage(
            event_id=item["event_id"],
            session_id=item["session_id"],
            material_code=item["material_code"],
            quantity=Decimal(item["quantity"]),
        )
        for item in payload["usages"]
    )
    settlement_payload = payload["closed_settlement"]
    settlement = None
    if settlement_payload is not None:
        lines = tuple(
            SettlementLine(
                code=line["code"],
                label=line["label"],
                quantity=Decimal(line["quantity"]),
                unit=line["unit"],
                unit_price_grosz=line["unit_price_grosz"],
                total_net_grosz=line["total_net_grosz"],
            )
            for line in settlement_payload["lines"]
        )
        settlement = Settlement(
            settlement_id=settlement_payload["settlement_id"],
            job_id=settlement_payload["job_id"],
            closed_at=_aware_datetime(settlement_payload["closed_at"]),
            lines=lines,
            total_net_grosz=settlement_payload["total_net_grosz"],
        )
    state = JobState(payload["state"])
    if (state is JobState.OPEN) != (settlement is None):
        raise ValueError("job state and settlement conflict")
    linked_ids = {link.session_id for link in links}
    if any(usage.session_id not in linked_ids for usage in usages):
        raise ValueError("material usage references an unlinked session")
    pricing_version = payload["pricing_version"]
    if type(pricing_version) is not int or pricing_version < 1:
        raise ValueError("pricing version must be a positive integer")
    corrections_payload = payload["price_corrections"]
    if not isinstance(corrections_payload, list):
        raise ValueError("price corrections must be a list")
    corrections: list[PriceCorrection] = []
    event_ids: set[str] = set()
    price_chain: dict[tuple[PriceField, str | None], int] = {}
    for item in corrections_payload:
        if not isinstance(item, dict):
            raise ValueError("price correction must be an object")
        event_id = item["event_id"]
        operator_id = item["operator_id"]
        reason = item["reason"]
        if not isinstance(event_id, str) or not event_id.strip():
            raise ValueError("correction event_id must be non-empty text")
        if event_id in event_ids:
            raise ValueError("correction event IDs must be unique")
        event_ids.add(event_id)
        if not isinstance(operator_id, str) or not operator_id.strip():
            raise ValueError("correction operator_id must be non-empty text")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("correction reason must be non-empty text")
        field = PriceField(item["field"])
        material_code = item["material_code"]
        if field is PriceField.COW_UNIT_PRICE:
            if material_code is not None:
                raise ValueError("cow correction cannot name a material")
        elif not isinstance(material_code, str) or not material_code.strip():
            raise ValueError("material correction requires material code")
        old_value = item["old_value_grosz"]
        new_value = item["new_value_grosz"]
        if type(old_value) is not int or old_value < 0:
            raise ValueError("old correction value must be integer grosze")
        if type(new_value) is not int or new_value < 0:
            raise ValueError("new correction value must be integer grosze")
        key = (field, material_code)
        if key in price_chain and price_chain[key] != old_value:
            raise ValueError("price correction history is discontinuous")
        price_chain[key] = new_value
        corrections.append(
            PriceCorrection(
                event_id=event_id.strip(),
                operator_id=operator_id.strip(),
                corrected_at=_aware_datetime(item["corrected_at"]),
                reason=reason.strip(),
                field=field,
                material_code=material_code.strip() if material_code is not None else None,
                old_value_grosz=old_value,
                new_value_grosz=new_value,
            )
        )
    if len(corrections) != pricing_version - 1:
        raise ValueError("pricing version and correction history conflict")
    for (field, material_code), expected_value in price_chain.items():
        active_value = (
            pricing.cow_unit_price_grosz
            if field is PriceField.COW_UNIT_PRICE
            else pricing.rate(material_code).unit_price_grosz
        )
        if active_value != expected_value:
            raise ValueError("active pricing and correction history conflict")
    return Job(
        job_id=base.job_id,
        farm_id=base.farm_id,
        operator_id=base.operator_id,
        opened_at=base.opened_at,
        pricing=base.pricing,
        planned_cows=base.planned_cows,
        state=state,
        completed_links=links,
        usages=usages,
        closed_settlement=settlement,
        pricing_version=pricing_version,
        price_corrections=tuple(corrections),
    )


class LocalJobStore:
    SNAPSHOT_SCHEMA_VERSION = 2

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, job: Job) -> None:
        if not isinstance(job, Job):
            raise ValueError("job must be a Job")
        payload = _serialize_job(job)
        envelope = {
            "schema_version": self.SNAPSHOT_SCHEMA_VERSION,
            "job": payload,
            "integrity": {"algorithm": "sha256", "digest": _digest(payload)},
        }
        target = self.root / f"{_safe_id(job.job_id)}.job.json"
        temp = target.with_suffix(target.suffix + ".tmp")
        serialized = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
        try:
            with temp.open("w", encoding="utf-8") as handle:
                handle.write(serialized)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp, target)
            self._fsync_directory()
        except BaseException:
            temp.unlink(missing_ok=True)
            raise

    def load(self, job_id: str) -> Job:
        safe_job_id = _safe_id(job_id)
        path = self.root / f"{safe_job_id}.job.json"
        if not path.is_file():
            raise KeyError(job_id)
        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
            payload = envelope["job"]
            if envelope["schema_version"] != self.SNAPSHOT_SCHEMA_VERSION:
                raise ValueError("unsupported job schema")
            if envelope["integrity"] != {
                "algorithm": "sha256",
                "digest": _digest(payload),
            }:
                raise ValueError("job snapshot integrity mismatch")
            job = _deserialize_job(payload)
            if job.job_id != safe_job_id:
                raise ValueError("job identifier mismatch")
            return job
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid persisted job: {job_id}") from exc

    def list_jobs(self) -> tuple[Job, ...]:
        suffix = ".job.json"
        job_ids = tuple(
            sorted(path.name[: -len(suffix)] for path in self.root.glob(f"*{suffix}"))
        )
        return tuple(self.load(job_id) for job_id in job_ids)

    def _fsync_directory(self) -> None:
        if not hasattr(os, "O_DIRECTORY"):
            return
        descriptor = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
