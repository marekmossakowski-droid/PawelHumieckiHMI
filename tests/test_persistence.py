import json
import tempfile
import unittest
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

    def test_amendment_log_is_append_only_and_ordered(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            session = Session.new()
            store.append_amendment(session.session_id, "operator-note", {"text": "first"})
            store.append_amendment(session.session_id, "operator-note", {"text": "second"})

            amendments = store.read_amendments(session.session_id)

            self.assertEqual([item["payload"]["text"] for item in amendments], ["first", "second"])
            self.assertEqual([item["sequence"] for item in amendments], [1, 2])

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
