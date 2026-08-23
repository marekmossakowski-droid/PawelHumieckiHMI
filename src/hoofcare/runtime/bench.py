from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


_ALLOWED_MODE = "SYNTHETIC_TEST_ONLY"


@dataclass(frozen=True)
class BenchRuntimeConfig:
    mode: str
    data_dir: str
    report_dir: str
    network_enabled: bool = False
    kvk_connected: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.mode, str):
            raise ValueError("bench runtime mode must be a string")
        if not isinstance(self.data_dir, str) or not isinstance(self.report_dir, str):
            raise ValueError("bench runtime directories must be strings")
        if type(self.network_enabled) is not bool or type(self.kvk_connected) is not bool:
            raise ValueError("bench runtime connection flags must be booleans")
        if self.mode != _ALLOWED_MODE:
            raise ValueError("bench runtime mode must be SYNTHETIC_TEST_ONLY")
        if self.network_enabled:
            raise ValueError("network is not authorized for bench runtime")
        if self.kvk_connected:
            raise ValueError("KVK connection is not authorized for bench runtime")
        if not self.data_dir.strip() or not self.report_dir.strip():
            raise ValueError("bench runtime directories must be non-empty")

    @classmethod
    def from_json_file(cls, path: str | Path) -> "BenchRuntimeConfig":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("bench runtime config must be a JSON object")
        expected = {"mode", "data_dir", "report_dir", "network_enabled", "kvk_connected"}
        if set(payload) != expected:
            raise ValueError("bench runtime config fields do not match canonical schema")
        return cls(
            mode=payload["mode"],
            data_dir=payload["data_dir"],
            report_dir=payload["report_dir"],
            network_enabled=payload["network_enabled"],
            kvk_connected=payload["kvk_connected"],
        )


def launch_bench_runtime(config: BenchRuntimeConfig) -> dict[str, object]:
    data_dir = Path(config.data_dir)
    report_dir = Path(config.report_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    return {
        "mode": config.mode,
        "data_dir": str(data_dir),
        "report_dir": str(report_dir),
        "network_enabled": False,
        "kvk_connected": False,
        "runtime_ready": True,
    }
