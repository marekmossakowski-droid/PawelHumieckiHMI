from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from hoofcare.hmi.gen1.shell import OwnerGateState, unlock_owner_zone
from hoofcare.integration.job_settlement import SyntheticJobSettlementScenario


@dataclass(frozen=True)
class Gen1CompleteScenarioResult:
    completed_cows: int
    total_label: str
    prices_hidden_during_treatment: bool
    owner_zone_expired_after_idle: bool
    dtools_manifest_status: str
    restart_consistent: bool


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _validate_dtools_manifest_offline(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("DTools manifest is unavailable or invalid JSON") from exc

    if data.get("schema_version") != 1:
        raise ValueError("DTools manifest schema is not supported")
    if data.get("profile_id") != "gl100e-landscape-v1":
        raise ValueError("DTools manifest does not target GL100E")
    if data.get("canvas") != {"width": 1024, "height": 600}:
        raise ValueError("DTools manifest canvas is not 1024x600")

    safety = data.get("safety_scope")
    if not isinstance(safety, dict):
        raise ValueError("DTools manifest safety scope is missing")
    if safety.get("data") != "SYNTHETIC_TEST_ONLY" or safety.get("device_access") is not False:
        raise ValueError("DTools manifest exceeds synthetic offline scope")

    native = data.get("native_artifact")
    if not isinstance(native, dict):
        raise ValueError("DTools native artifact status is missing")
    if native.get("status") not in {
        "NATIVE_DTOOLS_ARTIFACT_REQUIRED",
        "OFFLINE_COMPILE_VERIFIED",
    }:
        raise ValueError("DTools native artifact status is not truthful")

    screens = data.get("screens")
    if not isinstance(screens, list) or not screens:
        raise ValueError("DTools manifest screens are missing")
    route_ids = [screen.get("route_id") for screen in screens if isinstance(screen, dict)]
    if len(route_ids) != len(screens) or len(route_ids) != len(set(route_ids)):
        raise ValueError("DTools manifest route coverage is invalid")

    return "VALIDATED_OFFLINE"


def run_complete_gen1_synthetic_scenario() -> Gen1CompleteScenarioResult:
    with TemporaryDirectory(prefix="hoofcare-g1-") as temp_dir:
        settlement = SyntheticJobSettlementScenario(Path(temp_dir)).run()

    if not settlement.restart_consistent:
        raise ValueError("Generation 1 durable restart verification failed")
    if settlement.work_prices_visible:
        raise ValueError("prices must stay hidden during routine treatment work")

    now = datetime(2026, 8, 24, 8, tzinfo=timezone.utc)
    owner_session = unlock_owner_zone("123456", now, OwnerGateState("123456"))
    if not owner_session.authorized or owner_session.expires_at is None:
        raise ValueError("synthetic owner session could not be established")
    owner_zone_expired = not owner_session.is_active(owner_session.expires_at)

    manifest_status = _validate_dtools_manifest_offline(
        _repository_root() / "dtools" / "gl100e" / "manifest.json"
    )

    return Gen1CompleteScenarioResult(
        completed_cows=settlement.completed_cows,
        total_label=settlement.total_label,
        prices_hidden_during_treatment=not settlement.work_prices_visible,
        owner_zone_expired_after_idle=owner_zone_expired,
        dtools_manifest_status=manifest_status,
        restart_consistent=settlement.restart_consistent,
    )
