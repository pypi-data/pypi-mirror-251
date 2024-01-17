# confidence_calculator/tests/test_calculator.py

import unittest
from confidence_calculator.calculator import calculate_confidence

class TestCalculator(unittest.TestCase):

    def test_calculate_confidence(self):
        csv_path = "path/to/your/test.csv"  # Update with an actual CSV path
        confidence_level = 0.95
        result = calculate_confidence(csv_path, confidence_level)
        self.assertTrue(isinstance(result, tuple))
