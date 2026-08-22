from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable


class ObservationQuality(str, Enum):
    GOOD = "GOOD"
    UNKNOWN = "UNKNOWN"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class Observation:
    kind: str
    value: Any = None
    name: str | None = None
    simulated: bool = True
    observed_at: datetime | None = None
    source_id: str = "SIMULATED_UNKNOWN"
    quality: ObservationQuality = ObservationQuality.UNKNOWN
    stale: bool = False

    def __post_init__(self) -> None:
        observed_at = self.observed_at or datetime.now(timezone.utc)
        if observed_at.tzinfo is None or observed_at.utcoffset() is None:
            raise ValueError("observation timestamp must be timezone-aware")
        if not self.source_id.strip():
            raise ValueError("observation source_id must be non-empty")
        object.__setattr__(self, "observed_at", observed_at.astimezone(timezone.utc))


class SimulatedRfidAdapter:
    def __init__(self, identifiers: Iterable[str]):
        self._queue = list(identifiers)

    def read(self) -> Observation:
        if not self._queue:
            return Observation(
                kind="RFID_UNAVAILABLE",
                value=None,
                source_id="SIMULATED_RFID",
                quality=ObservationQuality.UNKNOWN,
                stale=True,
            )
        return Observation(
            kind="RFID_OBSERVATION",
            value=self._queue.pop(0),
            source_id="SIMULATED_RFID",
            quality=ObservationQuality.GOOD,
            stale=False,
        )


class SimulatedKvkObservationAdapter:
    def __init__(self, observations: Iterable[dict[str, Any]]):
        self._queue = list(observations)

    def observe(self) -> Observation:
        if not self._queue:
            return Observation(
                kind="KVK_UNKNOWN",
                name=None,
                value=None,
                source_id="SIMULATED_KVK",
                quality=ObservationQuality.UNKNOWN,
                stale=True,
            )
        item = self._queue.pop(0)
        return Observation(
            kind="KVK_OBSERVATION",
            name=item.get("name"),
            value=item.get("value"),
            source_id="SIMULATED_KVK",
            quality=ObservationQuality.GOOD,
            stale=False,
        )
