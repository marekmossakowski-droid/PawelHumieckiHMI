import unittest

from hoofcare.hardware.bench_wiring import build_isolated_bench_bom


class BenchWiringBomTests(unittest.TestCase):
    def test_bom_matches_selected_gl100e_and_ks123_14dr_hardware(self):
        bom = build_isolated_bench_bom()
        self.assertEqual(bom.nominal_voltage_vdc, 24)
        self.assertTrue(bom.isolated_from_kvk)
        self.assertTrue(bom.uses_existing_24v_supply)
        self.assertIn("Kinco GL100E", bom.items)
        self.assertIn("Kinco KS123-14DR (8DI/6 relay DO)", bom.items)
        self.assertNotIn("24 VDC DIN power supply", bom.items)
        self.assertNotIn("8DI/8DO simulator I/O", bom.items)

    def test_bom_limits_rs485_to_hmi_io_bench_link(self):
        bom = build_isolated_bench_bom()
        self.assertEqual(bom.bench_bus, "RS485_MODBUS_RTU")
        self.assertEqual(bom.bench_bus_scope, "GL100E_TO_KS123_14DR_ONLY")

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
