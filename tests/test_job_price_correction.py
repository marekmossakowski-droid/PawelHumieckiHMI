from datetime import datetime, timezone
import importlib
import unittest

from tests.job_fixtures import completed_session, open_job_fixture


CORRECTED_AT = datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc)


def require_symbol(case: unittest.TestCase, module_name: str, symbol: str):
    module = importlib.import_module(module_name)
    case.assertTrue(hasattr(module, symbol), f"{symbol} must exist")
    return getattr(module, symbol)


class JobPriceCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.PriceField = require_symbol(
            self, "hoofcare.domain.jobs", "PriceField"
        )

    def test_pawel_corrects_cow_price_before_first_completed_cow(self):
        job = open_job_fixture()

        changed = job.correct_price(
            "TEST-CORRECTION-1",
            "TEST-PAWEL",
            CORRECTED_AT,
            "Błąd przy wpisywaniu stawki",
            self.PriceField.COW_UNIT_PRICE,
            3600,
        )

        self.assertEqual(changed.pricing.cow_unit_price_grosz, 3600)
        self.assertEqual(changed.pricing_version, 2)
        correction = changed.price_corrections[0]
        self.assertEqual(correction.old_value_grosz, 3500)
        self.assertEqual(correction.new_value_grosz, 3600)
        self.assertEqual(correction.operator_id, "TEST-PAWEL")
        self.assertEqual(correction.corrected_at, CORRECTED_AT)

    def test_identical_retry_is_idempotent_and_conflict_fails_closed(self):
        job = open_job_fixture()
        args = (
            "TEST-CORRECTION-1",
            "TEST-PAWEL",
            CORRECTED_AT,
            "Literówka",
            self.PriceField.COW_UNIT_PRICE,
            3600,
        )

        once = job.correct_price(*args)

        self.assertEqual(once.correct_price(*args), once)
        with self.assertRaisesRegex(ValueError, "correction event payload conflict"):
            once.correct_price(*args[:-1], 3700)

    def test_first_completed_cow_freezes_all_prices(self):
        frozen = open_job_fixture().record_completed_session(
            completed_session("TEST-COW-1", "TEST-SESSION-1"),
            "TEST-COMPLETE-1",
        )

        self.assertTrue(frozen.pricing_frozen)
        with self.assertRaisesRegex(ValueError, "pricing is frozen"):
            frozen.correct_price(
                "TEST-CORRECTION-2",
                "TEST-PAWEL",
                datetime(2026, 8, 23, 9, tzinfo=timezone.utc),
                "Zmiana po pracy",
                self.PriceField.COW_UNIT_PRICE,
                3700,
            )


if __name__ == "__main__":
    unittest.main()
