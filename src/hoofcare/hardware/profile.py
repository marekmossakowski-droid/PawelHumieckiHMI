from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PhysicalPrototypeMode(str, Enum):
    ISOLATED_SYNTHETIC = "ISOLATED_SYNTHETIC"


@dataclass(frozen=True)
class HmiHardwareProfile:
    hmi_model: str
    io_model: str
    display_inches: float
    nominal_supply_vdc: int
    di_count: int
    do_count: int
    do_type: str
    existing_24v_supply: bool
    bench_bus: str
    bench_bus_scope: str
    mode: PhysicalPrototypeMode
    kvk_connection_allowed: bool
    real_farm_data_allowed: bool

    def __post_init__(self) -> None:
        if not isinstance(self.mode, PhysicalPrototypeMode):
            raise ValueError("physical prototype mode must remain isolated and synthetic")
        if self.mode is not PhysicalPrototypeMode.ISOLATED_SYNTHETIC:
            raise ValueError("only isolated synthetic prototype mode is authorized")
        if self.kvk_connection_allowed:
            raise ValueError("KVK connection is not authorized under IA-HC-004")
        if self.real_farm_data_allowed:
            raise ValueError("real farm data is not authorized under IA-HC-004")
        if self.display_inches <= 0:
            raise ValueError("display size must be positive")
        if self.nominal_supply_vdc <= 0:
            raise ValueError("nominal supply must be positive")
        if self.di_count < 0 or self.do_count < 0:
            raise ValueError("I/O counts cannot be negative")
        if self.bench_bus_scope != "GL100E_TO_KS123_14DR_ONLY":
            raise ValueError("bench bus scope must remain limited to GL100E and KS123-14DR")

    @classmethod
    def selected_bench(cls) -> "HmiHardwareProfile":
        return cls(
            hmi_model="Kinco GL100E",
            io_model="Kinco KS123-14DR",
            display_inches=10.1,
            nominal_supply_vdc=24,
            di_count=8,
            do_count=6,
            do_type="relay",
            existing_24v_supply=True,
            bench_bus="RS485_MODBUS_RTU",
            bench_bus_scope="GL100E_TO_KS123_14DR_ONLY",
            mode=PhysicalPrototypeMode.ISOLATED_SYNTHETIC,
            kvk_connection_allowed=False,
            real_farm_data_allowed=False,
        )

    @classmethod
    def prototype_10_inch(cls) -> "HmiHardwareProfile":
        """Compatibility alias for older bench code; returns the selected R0 hardware profile."""
        return cls.selected_bench()
