from pathlib import Path
import unittest


RECORD = Path("docs/verification/HC-G1-5-DTools-Bridge-Verification.md")


class DToolsBridgeVerificationRecordTests(unittest.TestCase):
    def test_approved_read_only_trial_is_bound_to_exact_evidence(self):
        payload = RECORD.read_text("utf-8")

        self.assertIn("`REAL_DTOOLS_PROBE=PASS_READ_ONLY`", payload)
        self.assertIn(
            "`e30362d7cf206bf02e28601635b47c4a1b27bc87`",
            payload,
        )
        self.assertIn(
            "`d4e7d5639a4e37a5249c36d29419e2612b954b5ec79bae3af15c05558ebacb06`",
            payload,
        )
        self.assertIn("`1920x1009`", payload)
        self.assertIn("`PROJECT_SAVE=NOT_AUTHORIZED`", payload)
        self.assertIn("`DEVICE_ACCESS=NONE`", payload)
        self.assertIn("`PLC_ACCESS=NONE`", payload)
        self.assertIn("`KVK_ACCESS=NONE`", payload)


if __name__ == "__main__":
    unittest.main()
