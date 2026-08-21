import unittest

from hoofcare.hardware.profile import HmiHardwareProfile, PhysicalPrototypeMode


class HardwareProfileTests(unittest.TestCase):
    def test_default_profile_is_isolated_and_synthetic(self):
        profile = HmiHardwareProfile.prototype_10_inch()
        self.assertEqual(profile.mode, PhysicalPrototypeMode.ISOLATED_SYNTHETIC)
        self.assertEqual(profile.nominal_supply_vdc, 24)
        self.assertGreaterEqual(profile.di_count, 0)
        self.assertGreaterEqual(profile.do_count, 0)
        self.assertFalse(profile.kvk_connection_allowed)
        self.assertFalse(profile.real_farm_data_allowed)

    def test_profile_exposes_no_live_machine_bus_enable(self):
        profile = HmiHardwareProfile.prototype_10_inch()
        forbidden = {"enable_kvk", "connect_kvk", "enable_can", "enable_modbus", "enable_serial", "actuate"}
        public = {name.lower() for name in dir(profile) if not name.startswith("_")}
        self.assertTrue(public.isdisjoint(forbidden))

    def test_profile_rejects_non_isolated_mode(self):
        with self.assertRaises(ValueError):
            HmiHardwareProfile(
                model="TEST",
                display_inches=10.1,
                nominal_supply_vdc=24,
                di_count=8,
                do_count=8,
                mode="LIVE_MACHINE",
                kvk_connection_allowed=False,
                real_farm_data_allowed=False,
            )


if __name__ == "__main__":
    unittest.main()
