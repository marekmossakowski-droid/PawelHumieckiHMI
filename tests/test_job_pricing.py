from decimal import Decimal
import importlib
import unittest


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        case.fail(f"{module_name} must exist")
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobPricingTests(unittest.TestCase):
    def setUp(self):
        self.MaterialRate = require_symbol(self, "hoofcare.domain.jobs", "MaterialRate")
        self.JobPricingSnapshot = require_symbol(
            self,
            "hoofcare.domain.jobs",
            "JobPricingSnapshot",
        )

    def test_material_line_uses_decimal_half_up_to_grosz(self):
        rate = self.MaterialRate("BLOCK", "Klocek", "szt.", 1855, 3, False, True)

        self.assertEqual(rate.line_total_grosz(Decimal("1.235")), 2291)

    def test_standard_scope_is_only_the_cow_rate(self):
        snapshot = self.JobPricingSnapshot(
            cow_unit_price_grosz=3500,
            additional_materials=(),
        )

        self.assertEqual(snapshot.cow_subtotal_grosz(40), 140000)
        self.assertEqual(snapshot.additional_materials, ())

    def test_local_material_extends_only_the_job_snapshot(self):
        original = self.JobPricingSnapshot(3500, ())
        local = self.MaterialRate("LOCAL-1", "Żel ochronny", "ml", 25, 1, True, True)

        extended = original.with_local_material(local)

        self.assertEqual(original.additional_materials, ())
        self.assertEqual(extended.additional_materials, (local,))

    def test_invalid_money_and_quantity_fail_closed(self):
        with self.assertRaises(ValueError):
            self.JobPricingSnapshot(-1, ())
        rate = self.MaterialRate("BLOCK", "Klocek", "szt.", 1855, 0, False, True)
        with self.assertRaises(ValueError):
            rate.line_total_grosz(Decimal("0.5"))

    def test_inactive_material_cannot_enter_a_new_snapshot(self):
        inactive = self.MaterialRate("OLD", "Wycofany", "szt.", 100, 0, False, False)

        with self.assertRaises(ValueError):
            self.JobPricingSnapshot(3500, (inactive,))


if __name__ == "__main__":
    unittest.main()
