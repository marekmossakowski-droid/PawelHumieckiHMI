from dataclasses import dataclass


@dataclass(frozen=True)
class BenchWiringBom:
    nominal_voltage_vdc: int
    isolated_from_kvk: bool
    kvk_connection_allowed: bool
    real_farm_data_allowed: bool
    items: tuple[str, ...]


def build_isolated_bench_bom() -> BenchWiringBom:
    return BenchWiringBom(
        nominal_voltage_vdc=24,
        isolated_from_kvk=True,
        kvk_connection_allowed=False,
        real_farm_data_allowed=False,
        items=(
            "10.1-inch HMI",
            "24 VDC DIN power supply",
            "8DI/8DO simulator I/O",
            "DIN rail terminal blocks",
            "bench fuse protection",
            "USB/RS-485 bench adapter",
            "momentary test switches",
            "indicator lamps",
        ),
    )
