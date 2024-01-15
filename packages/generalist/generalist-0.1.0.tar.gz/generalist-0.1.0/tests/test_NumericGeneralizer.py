from datetime import datetime
from unittest import TestCase

from parameterized import parameterized

from src.generalist import NumericGeneralizer


class TestNumericGeneralizer(TestCase):
    def setUp(self):
        self.generalizer = NumericGeneralizer.NumericGeneralizer(10)

    @parameterized.expand(
        [
            (1, True),
            (1.0, True),
            (datetime.now(), False),
            (None, False)
        ])
    def test_can_handle(self, item, expected):
        self.assertEqual(expected, self.generalizer.can_handle(item))

    @parameterized.expand([
        (12, 10),
        (123, 120),
        (1234, 1230),
    ])
    def test_inner_generalize(self, item, expected):
        result = self.generalizer.inner_generalize(item)
        self.assertEqual(expected, result)
