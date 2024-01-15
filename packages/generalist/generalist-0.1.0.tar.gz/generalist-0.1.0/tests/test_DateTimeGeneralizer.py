import unittest
from datetime import datetime

from parameterized import parameterized

from src.generalist.DateTimeGeneralizer import DateTimeGeneralizer


class TestDateTimeGeneralizer(unittest.TestCase):
    def setUp(self):
        self.generalizer = DateTimeGeneralizer()

    @parameterized.expand(
        [
            (datetime.now(), True),
            (1, False),
            (1.0, False),
            (None, False)
        ])
    def test_can_handle(self, item, expected):
        self.assertEqual(expected, self.generalizer.can_handle(item))

    @parameterized.expand(
        [
            (datetime(2024, 1, 10), datetime(2024, 1, 1)),
            (datetime(2024, 1, 10, 13, 15, 00), datetime(2024, 1, 10))
        ])
    def test_inner_generalize(self, item, expected):
        result = self.generalizer.inner_generalize(item)
        self.assertEqual(expected, result)
