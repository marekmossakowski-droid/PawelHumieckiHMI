import unittest
from datetime import datetime, timezone

import hoofcare.application as application
from hoofcare.adapters.simulated import Observation, SimulatedKvkObservationAdapter, SimulatedRfidAdapter


class ObservationProvenanceTests(unittest.TestCase):
    def test_observation_exposes_typed_provenance_and_staleness(self):
        observation = Observation(kind="TEST", value="x")
        self.assertTrue(hasattr(observation, "observed_at"))
        self.assertTrue(hasattr(observation, "source_id"))
        self.assertTrue(hasattr(observation, "quality"))
        self.assertTrue(hasattr(observation, "stale"))

    def test_simulated_rfid_observation_has_source_timestamp_quality(self):
        observation = SimulatedRfidAdapter(["TEST-COW-001"]).read()
        self.assertEqual(observation.source_id, "SIMULATED_RFID")
        self.assertIsInstance(observation.observed_at, datetime)
        self.assertIsNotNone(observation.observed_at.tzinfo)
        self.assertEqual(observation.observed_at.utcoffset(), timezone.utc.utcoffset(observation.observed_at))
        self.assertEqual(observation.quality, "GOOD")
        self.assertFalse(observation.stale)

    def test_empty_kvk_queue_is_explicitly_stale_unknown_quality(self):
        observation = SimulatedKvkObservationAdapter([]).observe()
        self.assertEqual(observation.source_id, "SIMULATED_KVK")
        self.assertEqual(observation.quality, "UNKNOWN")
        self.assertTrue(observation.stale)


class CapabilitySurfaceTests(unittest.TestCase):
    def test_application_exports_explicit_allowlist_only(self):
        allowed = getattr(application, "ALLOWED_ACTIONS", None)
        self.assertIsInstance(allowed, frozenset)
        self.assertEqual(
            allowed,
            frozenset({"create_session", "get_session", "resolve_identity", "open_reports", "back"}),
        )

    def test_unknown_or_machine_control_actions_fail_closed(self):
        dispatcher = getattr(application, "require_allowed_action", None)
        self.assertTrue(callable(dispatcher))
        for action in ("start_machine", "stop_machine", "reset_plc", "write_modbus", "set_hydraulics", "unknown"):
            with self.assertRaises(ValueError):
                dispatcher(action)

    def test_allowlisted_actions_are_accepted(self):
        dispatcher = getattr(application, "require_allowed_action", None)
        self.assertTrue(callable(dispatcher))
        for action in application.ALLOWED_ACTIONS:
            self.assertEqual(dispatcher(action), action)


if __name__ == "__main__":
    unittest.main()
