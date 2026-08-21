from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PhysicalPrototypeMode(str, Enum):
    ISOLATED_SYNTHETIC = "ISOLATED_SYNTHETIC"


@dataclass(frozen=True)
class HmiHardwareProfile:
    model: str
    display_inches: float
    nominal_supply_vdc: int
    di_count: int
    do_count: int
    mode: PhysicalPrototypeMode
    kvk_connection_allowed: bool
    real_farm_data_allowed: bool

    def __post_init__(self) -> None:
        if not isinstance(self.mode, PhysicalPrototypeMode):
            raise ValueError("physical prototype mode must remain isolated and synthetic")
        if self.mode is not PhysicalPrototypeMode.ISOLATED_SYNTHETIC:
            raise ValueError("only isolated synthetic prototype mode is authorized")
        if self.kvk_connection_allowed:
            raise ValueError("KVK connection is not authorized under IA-HC-002")
        if self.real_farm_data_allowed:
            raise ValueError("real farm data is not authorized under IA-HC-002")
        if self.display_inches <= 0:
            raise ValueError("display size must be positive")
        if self.nominal_supply_vdc <= 0:
            raise ValueError("nominal supply must be positive")
        if self.di_count < 0 or self.do_count < 0:
            raise ValueError("I/O counts cannot be negative")

    @classmethod
    def prototype_10_inch(cls) -> "HmiHardwareProfile":
        return cls(
            model="10-inch-class-prototype",
            display_inches=10.1,
            nominal_supply_vdc=24,
            di_count=8,
            do_count=8,
            mode=PhysicalPrototypeMode.ISOLATED_SYNTHETIC,
            kvk_connection_allowed=False,
            real_farm_data_allowed=False,
        )
