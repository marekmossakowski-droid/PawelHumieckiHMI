from importlib import import_module
from pathlib import Path
import unittest


class Generation1NavigationTests(unittest.TestCase):
    def test_route_graph_denies_owner_admin_without_owner_session(self):
        path = Path("src/hoofcare/hmi/gen1/navigation.py")
        self.assertTrue(path.is_file(), "hoofcare.hmi.gen1.navigation must exist")
        module = import_module("hoofcare.hmi.gen1.navigation")
        context = module.NavigationContext.synthetic_operator()

        decision = module.next_route(context, "open_owner_admin")

        self.assertEqual(decision.kind, module.RouteDecisionKind.DENY_WITH_REASON)
        self.assertEqual(decision.reason, "OWNER_UNLOCK_REQUIRED")


if __name__ == "__main__":
    unittest.main()
