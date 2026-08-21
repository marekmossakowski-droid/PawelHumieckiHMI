from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class Observation:
    kind: str
    value: Any = None
    name: str | None = None
    simulated: bool = True


class SimulatedRfidAdapter:
    def __init__(self, identifiers: Iterable[str]):
        self._queue = list(identifiers)

    def read(self) -> Observation:
        if not self._queue:
            return Observation(kind="RFID_UNAVAILABLE", value=None)
        return Observation(kind="RFID_OBSERVATION", value=self._queue.pop(0))


class SimulatedKvkObservationAdapter:
    def __init__(self, observations: Iterable[dict[str, Any]]):
        self._queue = list(observations)

    def observe(self) -> Observation:
        if not self._queue:
            return Observation(kind="KVK_UNKNOWN", name=None, value=None)
        item = self._queue.pop(0)
        return Observation(
            kind="KVK_OBSERVATION",
            name=item.get("name"),
            value=item.get("value"),
        )
