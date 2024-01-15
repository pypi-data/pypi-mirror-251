from unittest import TestCase

from src.generalist.BaseGeneralizer import BaseGeneralizer
from src.generalist.DataFly import DataflyAlgo
from src.generalist.NoneGeneralizer import NoneGeneralizer
from src.generalist.NumericGeneralizer import NumericGeneralizer
from src.generalist.StringMaskingGeneralizer import StringMaskingGeneralizer


class TestDataflyAlgo(TestCase):
    def test_anonymize_values(self):
        self.algo = DataflyAlgo({
            "age": NumericGeneralizer(100),
            "name": StringMaskingGeneralizer("*", 3, 5),
            "salary": NumericGeneralizer(1000)})
        item = TestItem("John", 320, 1023.7)
        anon = self.algo.anonymize([item])[0]

        self.assertEqual("Joh**", anon.name)
        self.assertEqual(300, anon.age)
        self.assertEqual(1000.0, anon.salary)

    def test_remove_values(self):
        self.algo = DataflyAlgo({"salary": NoneGeneralizer()})
        item = TestItem("John", 32, 1023.7)
        anon = self.algo.anonymize([item])[0]

        self.assertEqual("John", anon.name)
        self.assertEqual(32, anon.age)
        self.assertEqual(None, anon.salary)


class TestItem:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary
