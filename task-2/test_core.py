from json import load
from typing import TypedDict
from unittest import TestCase

from core import dollars_to_english_text, MAX_NUMBER, MIN_NUMBER

TEST_DATA_FILENAME = 'test-data.json'


class TestData(TypedDict):
    input: float
    output: str


class TestDollarsToEnglishText(TestCase):
    def setUp(self) -> None:
        with open(TEST_DATA_FILENAME) as f:
            self.data: list[TestData] = load(f)

    def test_raises_exception_when_value_is_bigger_than_max_number(self):
        with self.assertRaises(ValueError):
            dollars_to_english_text(MAX_NUMBER + 1)

    def test_raises_exception_when_value_is_less_or_equal_than_zero(self):
        with self.assertRaises(ValueError):
            dollars_to_english_text(MIN_NUMBER)
            dollars_to_english_text(-0.1)
    
    def test_cent_part_must_be_less_than_three_digits(self):
        with self.assertRaises(ValueError):
            dollars_to_english_text(0.125)

    def test_returns_correct_output_when_given_correct_input(self):
        for idx, item in enumerate(self.data):
            arg = item['input']
            result = item['output']
            with self.subTest(msg=f'Test {idx}', arg=arg):
                self.assertEqual(dollars_to_english_text(arg), result)
