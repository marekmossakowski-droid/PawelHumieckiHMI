from dataclasses import dataclass


@dataclass(frozen=True)
class BenchWiringBom:
    nominal_voltage_vdc: int
    isolated_from_kvk: bool
    uses_existing_24v_supply: bool
    bench_bus: str
    bench_bus_scope: str
    kvk_connection_allowed: bool
    real_farm_data_allowed: bool
    items: tuple[str, ...]


def build_isolated_bench_bom() -> BenchWiringBom:
    return BenchWiringBom(
        nominal_voltage_vdc=24,
        isolated_from_kvk=True,
        uses_existing_24v_supply=True,
        bench_bus="RS485_MODBUS_RTU",
        bench_bus_scope="GL100E_TO_KS123_14DR_ONLY",
        kvk_connection_allowed=False,
        real_farm_data_allowed=False,
        items=(
            "Kinco GL100E",
            "Kinco KS123-14DR (8DI/6 relay DO)",
            "existing isolated 24 VDC supply",
            "DIN rail terminal blocks",
            "bench fuse protection",
            "shielded RS485 bench cable",
            "momentary test switches",
            "indicator lamps / dedicated non-machine loads",
        ),
    )
