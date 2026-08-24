import json
from pathlib import Path
import tempfile
import unittest

from hoofcare.dtools_bridge.audit import AuditLog


class AuditLogTests(unittest.TestCase):
    def test_record_redacts_sensitive_values_recursively(self):
        with tempfile.TemporaryDirectory() as directory:
            log = AuditLog(Path(directory), session_id="session-01")

            operation = log.append(
                tool="dtools_set_text",
                arguments={
                    "token": "session-secret",
                    "nested": {
                        "value": "animal-secret",
                        "password": "operator-secret",
                    },
                },
                decision="ALLOW",
                result="OK",
            )

            record = json.loads(
                (Path(directory) / "audit.jsonl").read_text("utf-8")
            )
            payload = json.dumps(record)
            self.assertEqual(operation, 1)
            self.assertNotIn("session-secret", payload)
            self.assertNotIn("animal-secret", payload)
            self.assertNotIn("operator-secret", payload)
            self.assertEqual(record["arguments"]["token"], "[REDACTED]")
            self.assertEqual(
                record["arguments"]["nested"]["value"], "[REDACTED]"
            )

    def test_operation_numbers_are_monotonic_and_append_only(self):
        with tempfile.TemporaryDirectory() as directory:
            log = AuditLog(Path(directory), session_id="session-01")

            first = log.append("dtools_status", {}, "ALLOW", "OK")
            second = log.append("dtools_inspect", {}, "ALLOW", "OK")

            records = [
                json.loads(line)
                for line in (Path(directory) / "audit.jsonl")
                .read_text("utf-8")
                .splitlines()
            ]
            self.assertEqual((first, second), (1, 2))
            self.assertEqual(
                [record["operation_number"] for record in records], [1, 2]
            )

    def test_evidence_filename_contains_only_bounded_identifiers(self):
        with tempfile.TemporaryDirectory() as directory:
            log = AuditLog(Path(directory), session_id="session-01")
            operation = log.append("dtools_capture", {}, "ALLOW", "OK")

            evidence = log.record_evidence(b"synthetic-png", operation, "before")

            self.assertEqual(evidence, "session-01-000001-before.png")
            self.assertEqual(
                (Path(directory) / "evidence" / evidence).read_bytes(),
                b"synthetic-png",
            )

    def test_append_can_bind_evidence_references_to_same_record(self):
        with tempfile.TemporaryDirectory() as directory:
            log = AuditLog(Path(directory), session_id="session-01")

            operation = log.append(
                "dtools_capture",
                {},
                "ALLOW",
                "OK",
                evidence_before_image=b"before",
                evidence_after_image=b"after",
            )

            record = json.loads(
                (Path(directory) / "audit.jsonl").read_text("utf-8")
            )
            self.assertEqual(operation, 1)
            self.assertEqual(
                record["evidence_before"], "session-01-000001-before.png"
            )
            self.assertEqual(
                record["evidence_after"], "session-01-000001-after.png"
            )


if __name__ == "__main__":
    unittest.main()
