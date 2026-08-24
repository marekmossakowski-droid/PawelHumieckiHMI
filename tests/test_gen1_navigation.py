from importlib import import_module
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest


class Generation1NavigationTests(unittest.TestCase):
    def navigation(self):
        path = Path("src/hoofcare/hmi/gen1/navigation.py")
        self.assertTrue(path.is_file(), "hoofcare.hmi.gen1.navigation must exist")
        return import_module("hoofcare.hmi.gen1.navigation")

    def shell(self):
        path = Path("src/hoofcare/hmi/gen1/shell.py")
        self.assertTrue(path.is_file(), "hoofcare.hmi.gen1.shell must exist")
        return import_module("hoofcare.hmi.gen1.shell")

    def test_route_graph_denies_owner_admin_without_owner_session(self):
        module = self.navigation()
        context = module.NavigationContext.synthetic_operator()

        decision = module.next_route(context, "open_owner_admin")

        self.assertEqual(decision.kind, module.RouteDecisionKind.DENY_WITH_REASON)
        self.assertEqual(decision.reason, "OWNER_UNLOCK_REQUIRED")

    def test_owner_admin_is_allowed_for_an_active_owner_session(self):
        module = self.navigation()
        context = module.NavigationContext(
            current_route=module.Gen1Route.OWNER_DASHBOARD,
            owner_session_active=True,
        )

        decision = module.next_route(context, "open_owner_admin")

        self.assertEqual(decision.kind, module.RouteDecisionKind.ALLOW)
        self.assertEqual(decision.destination, module.Gen1Route.LOCAL_ADMIN)
        self.assertIsNone(decision.reason)

    def test_dirty_form_blocks_back_until_changes_are_resolved(self):
        module = self.navigation()
        context = module.NavigationContext(
            current_route=module.Gen1Route.JOB_PRICING,
            dirty_form=True,
        )

        decision = module.next_route(context, "back")

        self.assertEqual(decision.kind, module.RouteDecisionKind.DENY_WITH_REASON)
        self.assertEqual(decision.reason, "UNSAVED_CHANGES")

    def test_unknown_transition_routes_to_recovery(self):
        module = self.navigation()
        context = module.NavigationContext.synthetic_operator()

        decision = module.next_route(context, "unsupported_action")

        self.assertEqual(decision.kind, module.RouteDecisionKind.RECOVERY_REQUIRED)
        self.assertEqual(decision.destination, module.Gen1Route.RECONCILIATION)
        self.assertEqual(decision.reason, "INVALID_TRANSITION")

    def test_complete_treatment_route_sequence_matches_the_approved_screen_map(self):
        module = self.navigation()
        route = module.Gen1Route.ANIMAL_IDENTITY
        expected = (
            ("next", module.Gen1Route.LIMB_CLAW),
            ("next", module.Gen1Route.ZONE_LESION),
            ("next", module.Gen1Route.TREATMENT),
            ("next", module.Gen1Route.MATERIALS),
            ("next", module.Gen1Route.FOLLOW_UP),
            ("next", module.Gen1Route.COW_SUMMARY),
            ("complete_cow", module.Gen1Route.ANIMAL_IDENTITY),
        )

        for action, destination in expected:
            decision = module.next_route(module.NavigationContext(route), action)
            self.assertEqual(decision.kind, module.RouteDecisionKind.ALLOW)
            self.assertEqual(decision.destination, destination)
            route = destination

    def test_blocked_summary_can_open_explicit_reconciliation(self):
        module = self.navigation()

        decision = module.next_route(
            module.NavigationContext(module.Gen1Route.COW_SUMMARY),
            "open_reconciliation",
        )

        self.assertEqual(decision.kind, module.RouteDecisionKind.ALLOW)
        self.assertEqual(decision.destination, module.Gen1Route.RECONCILIATION)

    def test_route_catalog_contains_every_approved_generation_1_screen(self):
        module = self.navigation()

        self.assertEqual(
            {route.value for route in module.Gen1Route},
            {
                "G1-00", "G1-10", "G1-20", "G1-21", "G1-22",
                "G1-30", "G1-31", "G1-32", "G1-33", "G1-34", "G1-35", "G1-36",
                "G1-40", "G1-41", "G1-42", "G1-43",
                "G1-50", "G1-51", "G1-52", "G1-53", "G1-60",
            },
        )

    def test_operator_pricing_route_does_not_require_owner_unlock(self):
        module = self.navigation()
        context = module.NavigationContext(
            current_route=module.Gen1Route.JOB_SELECTION,
            owner_session_active=False,
        )

        decision = module.next_route(context, "open_job_pricing")

        self.assertEqual(decision.kind, module.RouteDecisionKind.ALLOW)
        self.assertEqual(decision.destination, module.Gen1Route.JOB_PRICING)

    def test_owner_pin_accepts_only_six_ascii_digits(self):
        module = self.shell()
        now = datetime(2026, 8, 24, 8, 0, tzinfo=timezone.utc)
        state = module.OwnerGateState(secret_pin="123456")

        for invalid_pin in ("12345", "1234567", "12A456", "１２３４５６"):
            result = module.unlock_owner_zone(invalid_pin, now, state)
            self.assertFalse(result.authorized)
            self.assertEqual(result.reason, "INVALID_PIN_FORMAT")

    def test_fifth_failed_pin_attempt_locks_for_five_minutes(self):
        module = self.shell()
        now = datetime(2026, 8, 24, 8, 0, tzinfo=timezone.utc)
        state = module.OwnerGateState(secret_pin="123456")

        for attempt in range(5):
            result = module.unlock_owner_zone("000000", now, state)
            state = result.gate_state
            self.assertEqual(state.failed_attempts, attempt + 1)

        self.assertFalse(result.authorized)
        self.assertEqual(result.reason, "OWNER_GATE_LOCKED")
        self.assertEqual(state.locked_until, now + timedelta(minutes=5))
        blocked = module.unlock_owner_zone("123456", now + timedelta(minutes=4), state)
        self.assertFalse(blocked.authorized)
        self.assertEqual(blocked.reason, "OWNER_GATE_LOCKED")

    def test_invalid_pin_format_is_counted_toward_lockout(self):
        module = self.shell()
        now = datetime(2026, 8, 24, 8, 0, tzinfo=timezone.utc)
        state = module.OwnerGateState(secret_pin="123456")

        for _ in range(5):
            result = module.unlock_owner_zone("12A456", now, state)
            state = result.gate_state

        self.assertEqual(state.failed_attempts, 5)
        self.assertEqual(state.locked_until, now + timedelta(minutes=5))
        self.assertEqual(result.reason, "OWNER_GATE_LOCKED")

    def test_expired_lockout_starts_a_new_failure_sequence(self):
        module = self.shell()
        now = datetime(2026, 8, 24, 8, 0, tzinfo=timezone.utc)
        locked = module.OwnerGateState(
            secret_pin="123456",
            failed_attempts=5,
            locked_until=now + timedelta(minutes=5),
        )

        result = module.unlock_owner_zone("000000", now + timedelta(minutes=5), locked)

        self.assertEqual(result.reason, "INVALID_PIN")
        self.assertEqual(result.gate_state.failed_attempts, 1)
        self.assertIsNone(result.gate_state.locked_until)

    def test_successful_owner_session_expires_after_ten_minutes_inactivity(self):
        module = self.shell()
        now = datetime(2026, 8, 24, 8, 0, tzinfo=timezone.utc)
        state = module.OwnerGateState(secret_pin="123456")

        session = module.unlock_owner_zone("123456", now, state)

        self.assertTrue(session.authorized)
        self.assertTrue(session.is_active(now + timedelta(minutes=9, seconds=59)))
        self.assertFalse(session.is_active(now + timedelta(minutes=10)))

    def test_owner_gate_rejects_naive_time(self):
        module = self.shell()
        state = module.OwnerGateState(secret_pin="123456")

        with self.assertRaisesRegex(ValueError, "timezone-aware"):
            module.unlock_owner_zone("123456", datetime(2026, 8, 24, 8, 0), state)


if __name__ == "__main__":
    unittest.main()
