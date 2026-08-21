import unittest

from hoofcare.hardware.bench_wiring import build_isolated_bench_bom


class BenchWiringBomTests(unittest.TestCase):
    def test_bom_is_24vdc_isolated_and_contains_required_items(self):
        bom = build_isolated_bench_bom()
        self.assertEqual(bom.nominal_voltage_vdc, 24)
        self.assertTrue(bom.isolated_from_kvk)
        self.assertIn("10.1-inch HMI", bom.items)
        self.assertIn("24 VDC DIN power supply", bom.items)
        self.assertIn("8DI/8DO simulator I/O", bom.items)

    def test_real_kvk_and_real_farm_data_are_forbidden(self):
        bom = build_isolated_bench_bom()
        self.assertFalse(bom.kvk_connection_allowed)
        self.assertFalse(bom.real_farm_data_allowed)

    def test_machine_bus_and_actuation_surfaces_do_not_exist(self):
        forbidden = {"connect_kvk", "modbus_machine", "can_machine", "command", "write", "actuate", "configure_kvk"}
        public = {name.lower() for name in dir(build_isolated_bench_bom()) if not name.startswith("_")}
        self.assertTrue(public.isdisjoint(forbidden))


if __name__ == "__main__":
    unittest.main()
