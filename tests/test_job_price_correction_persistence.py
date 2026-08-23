from datetime import datetime, timezone
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from hoofcare.domain.jobs import PriceField
from hoofcare.persistence.job_store import LocalJobStore

try:
    from tests.job_fixtures import open_job_fixture
except ModuleNotFoundError:
    from job_fixtures import open_job_fixture


CORRECTED_AT = datetime(2026, 8, 23, 8, 30, tzinfo=timezone.utc)


def corrected_open_job_fixture():
    return open_job_fixture().correct_price(
        "TEST-CORRECTION-1",
        "TEST-PAWEL",
        CORRECTED_AT,
        "Błąd stawki",
        PriceField.COW_UNIT_PRICE,
        3600,
    )


class JobPriceCorrectionPersistenceTests(unittest.TestCase):
    def test_corrected_job_round_trip_preserves_version_and_audit(self):
        job = corrected_open_job_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalJobStore(Path(tmp))
            store.save(job)

            self.assertEqual(store.load(job.job_id), job)

    def test_schema_v2_contains_complete_pricing_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = LocalJobStore(root)
            store.save(corrected_open_job_fixture())
            envelope = json.loads(
                (root / "TEST-JOB-1.job.json").read_text(encoding="utf-8")
            )

            self.assertEqual(envelope["schema_version"], 2)
            self.assertEqual(envelope["job"]["pricing_version"], 2)
            self.assertEqual(
                envelope["job"]["price_corrections"][0]["event_id"],
                "TEST-CORRECTION-1",
            )

    def test_failed_replace_preserves_previous_pricing_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalJobStore(Path(tmp))
            store.save(open_job_fixture())
            with mock.patch(
                "hoofcare.persistence.job_store.os.replace",
                side_effect=OSError("TEST-FAIL"),
            ):
                with self.assertRaises(OSError):
                    store.save(corrected_open_job_fixture())

            self.assertEqual(store.load("TEST-JOB-1").pricing_version, 1)

    def test_missing_correction_audit_fails_closed_even_with_valid_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = LocalJobStore(root)
            store.save(corrected_open_job_fixture())
            path = root / "TEST-JOB-1.job.json"
            envelope = json.loads(path.read_text(encoding="utf-8"))

            self.assertIn("price_corrections", envelope["job"])
            envelope["job"]["price_corrections"] = []
            encoded = json.dumps(
                envelope["job"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            envelope["integrity"]["digest"] = hashlib.sha256(encoded).hexdigest()
            path.write_text(
                json.dumps(envelope, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "invalid persisted job"):
                store.load("TEST-JOB-1")


if __name__ == "__main__":
    unittest.main()
