import tempfile
import unittest
from pathlib import Path

from hoofcare.persistence.local_store import LocalSessionStore


class LocalSessionStorePathSafetyTests(unittest.TestCase):
    def test_load_rejects_path_traversal_session_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            with self.assertRaises(ValueError):
                store.load("../outside")

    def test_amendment_paths_reject_path_traversal_session_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            with self.assertRaises(ValueError):
                store.append_amendment("../../outside", "operator-note", {"text": "x"})
            with self.assertRaises(ValueError):
                store.read_amendments("../../outside")

    def test_unsafe_separator_and_empty_session_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LocalSessionStore(Path(tmp) / "sessions")
            for session_id in ("", ".", "..", "a/b", "a\\b"):
                with self.subTest(session_id=session_id):
                    with self.assertRaises(ValueError):
                        store.load(session_id)


if __name__ == "__main__":
    unittest.main()
