import unittest
from datetime import datetime
import parameterized

from src.generalist.StringMaskingGeneralizer import StringMaskingGeneralizer


class TestStringMaskingGeneralizer(unittest.TestCase):
    def setUp(self):
        self.generalizer = StringMaskingGeneralizer('*')

    @parameterized.parameterized.expand([
        ("test", True),
        (datetime.now(), False),
        (1, False),
        (1.0, False),
        (None, False)
    ])
    def test_can_handle(self, item, expected):
        self.assertEqual(expected, self.generalizer.can_handle(item))

    @parameterized.parameterized.expand([
        "test",
        "testtesttesttest"
    ])
    def test_inner_generalize(self, item):
        result = self.generalizer.inner_generalize(item)
        self.assertEqual("**********", result)
