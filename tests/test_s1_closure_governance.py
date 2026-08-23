from pathlib import Path
import unittest


class S1ClosureGovernanceTests(unittest.TestCase):
    def test_s1_closure_record_captures_verified_final_merge(self):
        path = Path("docs/closure/HC-REQ-HC-002-S1-CLOSURE-001.md")
        self.assertTrue(path.is_file(), "REQ-HC-002-S1 closure record must exist")
        text = path.read_text(encoding="utf-8")
        self.assertIn("CLOSURE READY — PROJECT OWNER MERGE REQUIRED", text)
        self.assertIn("5c7ac7811fcb524191f226acecfc54f5bb921064", text)
        self.assertIn("53c4dbefad383446d4f64fffa52817f690777ec4", text)


if __name__ == "__main__":
    unittest.main()
