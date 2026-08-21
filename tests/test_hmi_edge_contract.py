import unittest

from hoofcare.application.contract import (
    BenchApplicationService,
    ContractError,
    ErrorCode,
)


class HmiEdgeContractTests(unittest.TestCase):
    def setUp(self):
        self.service = BenchApplicationService.in_memory()

    def test_create_session_returns_local_view_model(self):
        result = self.service.create_session(request_id="req-1")
        self.assertTrue(result.ok)
        self.assertEqual(result.data["state"], "IDENTITY_PENDING")
        self.assertIn("session_id", result.data)

    def test_unknown_session_is_explicit_not_found(self):
        result = self.service.get_session("missing")
        self.assertFalse(result.ok)
        self.assertEqual(result.error.code, ErrorCode.NOT_FOUND)

    def test_ambiguous_identity_remains_fail_closed(self):
        created = self.service.create_session(request_id="req-2")
        sid = created.data["session_id"]
        result = self.service.resolve_identity(
            sid,
            request_id="req-3",
            candidates=("cow-a", "cow-b"),
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.data["state"], "IDENTITY_PENDING")
        self.assertIsNone(result.data["animal_id"])

    def test_confirmed_identity_advances_session(self):
        created = self.service.create_session(request_id="req-4")
        sid = created.data["session_id"]
        result = self.service.resolve_identity(
            sid,
            request_id="req-5",
            confirmed_animal_id="cow-001",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.data["state"], "IN_PROGRESS")
        self.assertEqual(result.data["animal_id"], "cow-001")

    def test_invalid_identity_request_is_explicit_contract_error(self):
        created = self.service.create_session(request_id="req-6")
        sid = created.data["session_id"]
        result = self.service.resolve_identity(sid, request_id="req-7")
        self.assertFalse(result.ok)
        self.assertEqual(result.error.code, ErrorCode.INVALID_REQUEST)

    def test_duplicate_request_id_is_idempotent(self):
        first = self.service.create_session(request_id="same-request")
        second = self.service.create_session(request_id="same-request")
        self.assertEqual(first.data["session_id"], second.data["session_id"])

    def test_contract_exposes_no_kvk_actuation_surface(self):
        forbidden = {
            "command_kvk", "write_kvk", "open_gate", "close_gate",
            "set_valve", "lift", "winch", "start_hydraulics",
        }
        available = set(dir(self.service))
        self.assertTrue(forbidden.isdisjoint(available))

    def test_contract_error_is_serializable(self):
        error = ContractError(ErrorCode.INVALID_REQUEST, "bad request")
        self.assertEqual(
            error.to_dict(),
            {"code": "INVALID_REQUEST", "message": "bad request"},
        )


if __name__ == "__main__":
    unittest.main()
