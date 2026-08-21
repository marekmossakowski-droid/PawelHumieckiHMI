import unittest

from hoofcare.adapters.simulated import (
    SimulatedKvkObservationAdapter,
    SimulatedRfidAdapter,
)


class SimulatedAdaptersTests(unittest.TestCase):
    def test_rfid_returns_scripted_identifier(self):
        adapter = SimulatedRfidAdapter(["COW-001"])
        event = adapter.read()
        self.assertEqual(event.kind, "RFID_OBSERVATION")
        self.assertEqual(event.value, "COW-001")
        self.assertTrue(event.simulated)

    def test_rfid_empty_queue_is_explicitly_unavailable(self):
        adapter = SimulatedRfidAdapter([])
        event = adapter.read()
        self.assertEqual(event.kind, "RFID_UNAVAILABLE")
        self.assertIsNone(event.value)
        self.assertTrue(event.simulated)

    def test_kvk_observations_are_read_only_and_scripted(self):
        adapter = SimulatedKvkObservationAdapter([
            {"name": "ANIMAL_PRESENT", "value": True},
            {"name": "LEFT_FRONT_SUPPORTED", "value": False},
        ])
        first = adapter.observe()
        second = adapter.observe()
        self.assertEqual(first.kind, "KVK_OBSERVATION")
        self.assertEqual(first.name, "ANIMAL_PRESENT")
        self.assertIs(first.value, True)
        self.assertEqual(second.name, "LEFT_FRONT_SUPPORTED")
        self.assertIs(second.value, False)
        self.assertTrue(first.simulated)

    def test_kvk_unknown_when_no_scripted_observation(self):
        adapter = SimulatedKvkObservationAdapter([])
        observation = adapter.observe()
        self.assertEqual(observation.kind, "KVK_UNKNOWN")
        self.assertIsNone(observation.name)
        self.assertIsNone(observation.value)

    def test_kvk_adapter_exposes_no_command_surface(self):
        adapter = SimulatedKvkObservationAdapter([])
        forbidden = {"command", "write", "configure", "actuate", "set_output", "open_gate", "close_gate"}
        self.assertTrue(forbidden.isdisjoint(set(dir(adapter))))


if __name__ == "__main__":
    unittest.main()
