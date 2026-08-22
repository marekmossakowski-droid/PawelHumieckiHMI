import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from hoofcare.domain.session import (
    AnimalIdentityResolution,
    Session,
    SessionEvent,
    SessionEventType,
    SessionState,
)
from hoofcare.persistence.local_store import LocalSessionStore


class LocalSessionStoreTests(unittest.TestCase):
    def test_save_and_reload_preserves_nonterminal_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            session = Session.new().apply(
                SessionEvent(
                    event_id="evt-identity",
                    event_type=SessionEventType.IDENTITY_RESOLVED,
                    payload=AnimalIdentityResolution.confirmed("cow-001"),
                )
            )
            store.save(session)

            restored = store.load(session.session_id)

            self.assertEqual(restored.session_id, session.session_id)
            self.assertEqual(restored.state, SessionState.IN_PROGRESS)
            self.assertEqual(restored.animal_id, "cow-001")
            self.assertEqual(restored.applied_event_ids, ("evt-identity",))

    def test_save_is_atomic_and_latest_snapshot_replaces_previous_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            store = LocalSessionStore(root)
            session = Session.new()
            store.save(session)
            progressed = session.apply(
                SessionEvent(
                    event_id="evt-identity",
                    event_type=SessionEventType.IDENTITY_RESOLVED,
                    payload=AnimalIdentityResolution.confirmed("cow-002"),
                )
            )
            store.save(progressed)

            restored = store.load(session.session_id)
            self.assertEqual(restored.state, SessionState.IN_PROGRESS)
            self.assertFalse(any(path.suffix == ".tmp" for path in root.iterdir()))

    def test_snapshot_has_schema_version_and_integrity_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            store = LocalSessionStore(root)
            session = Session.new()
            store.save(session)

            envelope = json.loads((root / f"{session.session_id}.json").read_text(encoding="utf-8"))

            self.assertEqual(envelope["schema_version"], 1)
            self.assertEqual(envelope["integrity"]["algorithm"], "sha256")
            self.assertEqual(len(envelope["integrity"]["digest"]), 64)
            self.assertEqual(envelope["session"]["session_id"], session.session_id)

    def test_snapshot_integrity_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            store = LocalSessionStore(root)
            session = Session.new()
            store.save(session)
            snapshot = root / f"{session.session_id}.json"
            envelope = json.loads(snapshot.read_text(encoding="utf-8"))
            envelope["session"]["state"] = SessionState.COMPLETED.value
            snapshot.write_text(json.dumps(envelope, sort_keys=True), encoding="utf-8")

            with self.assertRaises(ValueError):
                store.load(session.session_id)

    def test_amendment_log_is_append_only_ordered_and_has_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            session = Session.new()
            store.append_amendment(
                session.session_id,
                "operator-note",
                {"text": "first"},
                actor_id="operator-test",
                source="bench-hmi",
                context={"reason": "synthetic-test"},
            )
            store.append_amendment(
                session.session_id,
                "operator-note",
                {"text": "second"},
                actor_id="operator-test",
                source="bench-hmi",
                context={"reason": "synthetic-test"},
            )

            amendments = store.read_amendments(session.session_id)

            self.assertEqual([item["payload"]["text"] for item in amendments], ["first", "second"])
            self.assertEqual([item["sequence"] for item in amendments], [1, 2])
            self.assertEqual([item["actor_id"] for item in amendments], ["operator-test", "operator-test"])
            self.assertEqual([item["source"] for item in amendments], ["bench-hmi", "bench-hmi"])
            self.assertTrue(all(item["record_id"] for item in amendments))
            self.assertEqual(len({item["record_id"] for item in amendments}), 2)
            self.assertTrue(all(item["timestamp_utc"].endswith("Z") for item in amendments))
            self.assertEqual(amendments[0]["context"], {"reason": "synthetic-test"})
            self.assertTrue(all(item["schema_version"] == 1 for item in amendments))
            self.assertTrue(all(item["integrity"]["algorithm"] == "sha256" for item in amendments))
            self.assertTrue(all(len(item["integrity"]["digest"]) == 64 for item in amendments))

    def test_amendment_integrity_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            store = LocalSessionStore(root)
            session = Session.new()
            store.append_amendment(
                session.session_id,
                "operator-note",
                {"text": "original"},
                actor_id="operator-test",
                source="bench-hmi",
                context={"reason": "synthetic-test"},
            )
            path = root / f"{session.session_id}.amendments.jsonl"
            record = json.loads(path.read_text(encoding="utf-8").strip())
            record["payload"]["text"] = "tampered"
            path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                store.read_amendments(session.session_id)

    def test_concurrent_amendments_receive_unique_contiguous_sequences(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            session = Session.new()

            def append(index: int) -> None:
                store.append_amendment(
                    session.session_id,
                    "operator-note",
                    {"index": index},
                    actor_id="operator-test",
                    source="bench-hmi",
                    context={"batch": "concurrency-test"},
                )

            with ThreadPoolExecutor(max_workers=8) as executor:
                list(executor.map(append, range(20)))

            amendments = store.read_amendments(session.session_id)
            self.assertEqual([item["sequence"] for item in amendments], list(range(1, 21)))
            self.assertEqual(len({item["record_id"] for item in amendments}), 20)

    def test_corrupt_snapshot_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            store = LocalSessionStore(root)
            session = Session.new()
            store.save(session)
            snapshot = root / f"{session.session_id}.json"
            snapshot.write_text("{not-json", encoding="utf-8")

            with self.assertRaises(ValueError):
                store.load(session.session_id)

    def test_missing_session_raises_key_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            with self.assertRaises(KeyError):
                store.load("missing")


if __name__ == "__main__":
    unittest.main()
