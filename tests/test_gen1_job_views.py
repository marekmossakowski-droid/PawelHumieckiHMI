from pathlib import Path
import unittest


class Gen1JobViewsContractTests(unittest.TestCase):
    def test_generation_1_job_views_surface_exists(self):
        module_path = (
            Path(__file__).parents[1]
            / "src"
            / "hoofcare"
            / "hmi"
            / "gen1"
            / "job_views.py"
        )
        self.assertTrue(module_path.is_file(), "hoofcare.hmi.gen1.job_views must exist")


if __name__ == "__main__":
    unittest.main()
