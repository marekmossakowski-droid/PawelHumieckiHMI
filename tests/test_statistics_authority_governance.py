from pathlib import Path
import unittest


class StatisticsAuthorityGovernanceTests(unittest.TestCase):
    def test_statistics_authority_package_is_complete_and_inactive(self):
        requirement = Path("docs/requirements/REQ-HC-002-S1_Job_Statistics_and_Final_Settlement_v0.1.md")
        authority = Path("governance/IA-HC-007-S1_Job_Statistics_and_Final_Settlement_Authority_v0.1.md")
        decision = Path("docs/decisions/HC-REQ-HC-002-S1-PREPARATION-DECISION-001.md")
        for path in (requirement, authority, decision):
            self.assertTrue(path.is_file(), f"required governance surface missing: {path}")
        self.assertIn("PROPOSED / NOT ACTIVE", authority.read_text(encoding="utf-8"))
        self.assertIn("RUNTIME NOT AUTHORIZED", decision.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
