import unittest

from hoofcare.hardware.profile import HmiHardwareProfile, PhysicalPrototypeMode


class HardwareProfileTests(unittest.TestCase):
    def test_selected_profile_matches_gl100e_and_ks123_14dr(self):
        profile = HmiHardwareProfile.selected_bench()
        self.assertEqual(profile.hmi_model, "Kinco GL100E")
        self.assertEqual(profile.io_model, "Kinco KS123-14DR")
        self.assertEqual(profile.display_inches, 10.1)
        self.assertEqual(profile.nominal_supply_vdc, 24)
        self.assertEqual(profile.di_count, 8)
        self.assertEqual(profile.do_count, 6)
        self.assertEqual(profile.do_type, "relay")
        self.assertEqual(profile.mode, PhysicalPrototypeMode.ISOLATED_SYNTHETIC)
        self.assertFalse(profile.kvk_connection_allowed)
        self.assertFalse(profile.real_farm_data_allowed)

    def test_profile_uses_existing_isolated_24v_supply_and_local_bench_rs485_only(self):
        profile = HmiHardwareProfile.selected_bench()
        self.assertTrue(profile.existing_24v_supply)
        self.assertEqual(profile.bench_bus, "RS485_MODBUS_RTU")
        self.assertEqual(profile.bench_bus_scope, "GL100E_TO_KS123_14DR_ONLY")

    def test_profile_exposes_no_live_machine_bus_enable(self):
        profile = HmiHardwareProfile.selected_bench()
        forbidden = {"enable_kvk", "connect_kvk", "enable_can", "enable_machine_modbus", "enable_serial", "actuate"}
        public = {name.lower() for name in dir(profile) if not name.startswith("_")}
        self.assertTrue(public.isdisjoint(forbidden))

    def test_profile_rejects_non_isolated_mode(self):
        with self.assertRaises(ValueError):
            HmiHardwareProfile(
                hmi_model="TEST",
                io_model="TEST",
                display_inches=10.1,
                nominal_supply_vdc=24,
                di_count=8,
                do_count=6,
                do_type="relay",
                existing_24v_supply=True,
                bench_bus="RS485_MODBUS_RTU",
                bench_bus_scope="GL100E_TO_KS123_14DR_ONLY",
                mode="LIVE_MACHINE",
                kvk_connection_allowed=False,
                real_farm_data_allowed=False,
            )


if __name__ == "__main__":
    unittest.main()
