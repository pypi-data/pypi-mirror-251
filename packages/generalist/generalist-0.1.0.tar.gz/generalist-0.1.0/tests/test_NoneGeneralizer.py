from datetime import datetime
from unittest import TestCase

from parameterized import parameterized

from src.generalist.NoneGeneralizer import NoneGeneralizer


class TestNoneGeneralizer(TestCase):
    def setUp(self):
        self.generalizer = NoneGeneralizer()

    @parameterized.expand(
        [
            (1, True),
            (1.0, True),
            (datetime.now(), True),
            (None, True)
        ])
    def test_can_handle(self, item, expected):
        self.assertEqual(expected, self.generalizer.can_handle(item))

    @parameterized.expand([12, "a", 1.0, datetime.now(), None])
    def test_inner_generalize(self, item):
        result = self.generalizer.inner_generalize(item)
        self.assertEqual(None, result)
