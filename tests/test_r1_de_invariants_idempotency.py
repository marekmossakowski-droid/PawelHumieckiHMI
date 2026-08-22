import unittest

from hoofcare.application.contract import BenchApplicationService
from hoofcare.domain.session import (
    AnimalIdentityResolution,
    IdentityStatus,
    Session,
    SessionState,
)


class DomainInvariantTests(unittest.TestCase):
    def test_confirmed_identity_requires_matching_session_animal_id(self):
        with self.assertRaises(ValueError):
            Session(
                session_id="session-1",
                state=SessionState.IN_PROGRESS,
                identity=AnimalIdentityResolution(
                    status=IdentityStatus.CONFIRMED,
                    animal_id="cow-001",
                ),
                animal_id="cow-002",
            )

    def test_nonconfirmed_identity_cannot_carry_session_animal_id(self):
        with self.assertRaises(ValueError):
            Session(
                session_id="session-2",
                state=SessionState.IDENTITY_PENDING,
                identity=AnimalIdentityResolution.unresolved(),
                animal_id="cow-001",
            )

    def test_identity_resolution_direct_construction_enforces_status_shape(self):
        with self.assertRaises(ValueError):
            AnimalIdentityResolution(
                status=IdentityStatus.CONFIRMED,
                animal_id=None,
            )
        with self.assertRaises(ValueError):
            AnimalIdentityResolution(
                status=IdentityStatus.AMBIGUOUS,
                candidates=("cow-001",),
            )


class IdempotencyIsolationTests(unittest.TestCase):
    def test_same_request_id_on_different_operations_does_not_return_unrelated_result(self):
        service = BenchApplicationService.in_memory()
        created = service.create_session(request_id="req-shared")
        session_id = created.data["session_id"]

        resolved = service.resolve_identity(
            session_id,
            request_id="req-shared",
            confirmed_animal_id="cow-001",
        )

        self.assertTrue(resolved.ok)
        self.assertEqual(resolved.data["session_id"], session_id)
        self.assertEqual(resolved.data["animal_id"], "cow-001")
        self.assertEqual(resolved.data["identity_status"], "CONFIRMED")

    def test_same_request_id_on_different_sessions_is_isolated(self):
        service = BenchApplicationService.in_memory()
        first = service.create_session(request_id="create-1")
        second = service.create_session(request_id="create-2")

        result_1 = service.resolve_identity(
            first.data["session_id"],
            request_id="resolve-shared",
            confirmed_animal_id="cow-001",
        )
        result_2 = service.resolve_identity(
            second.data["session_id"],
            request_id="resolve-shared",
            confirmed_animal_id="cow-002",
        )

        self.assertEqual(result_1.data["animal_id"], "cow-001")
        self.assertEqual(result_2.data["animal_id"], "cow-002")
        self.assertNotEqual(result_1.data["session_id"], result_2.data["session_id"])


if __name__ == "__main__":
    unittest.main()
