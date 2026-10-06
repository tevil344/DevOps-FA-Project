"""Fast unit tests that run in CI without loading the large ML models."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))

from app.observability import metric_path  # noqa: E402


class Request:
    def __init__(self, path):
        self.path = path


class MetricPathTests(unittest.TestCase):
    def test_known_api_paths_are_low_cardinality(self):
        self.assertEqual(metric_path(Request('/api/predict/')), '/api/predict/')
        self.assertEqual(metric_path(Request('/api/auth/login/')), '/api/auth/')
        self.assertEqual(metric_path(Request('/api/health/')), '/api/health/')

    def test_dynamic_and_unknown_paths_do_not_become_labels(self):
        self.assertEqual(metric_path(Request('/api/disease/Tomato_Early_Blight/')), 'other')
        self.assertEqual(metric_path(Request('/anything/else')), 'other')


if __name__ == '__main__':
    unittest.main()
