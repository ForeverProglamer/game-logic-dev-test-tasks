from pathlib import Path
from unittest import TestCase

from core import Treasury
from utils import TreasuryReader

SMALL_INPUT_FILE = Path('Treasure_1_Small.in')

CASES: list[Treasury] = [
    {
        'keys': [13, 13],
        'chests': [
            {'number': 1, 'type': 13, 'keys': []},
            {'number': 2, 'type': 13, 'keys': [13]},
            {'number': 3, 'type': 13, 'keys': [13]},
            {'number': 4, 'type': 13, 'keys': [13]},
            {'number': 5, 'type': 13, 'keys': []},
            {'number': 6, 'type': 13, 'keys': []},
            {'number': 7, 'type': 13, 'keys': [13, 13]},
            {'number': 8, 'type': 13, 'keys': [13]},
            {'number': 9, 'type': 13, 'keys': [13]},
        ]
    },
    {
        'keys': [3],
        'chests': [
            {'number': 1, 'type': 4, 'keys': [1]},
            {'number': 2, 'type': 3, 'keys': [3, 3, 2]},
            {'number': 3, 'type': 4, 'keys': [1]},
            {'number': 4, 'type': 4, 'keys': [2]},
            {'number': 5, 'type': 1, 'keys': [2, 4, 2, 4, 3]},
            {'number': 6, 'type': 4, 'keys': [4, 3]},
            {'number': 7, 'type': 4, 'keys': []},
            {'number': 8, 'type': 4, 'keys': [2]},
            {'number': 9, 'type': 4, 'keys': [2, 4, 4]},
            {'number': 10, 'type': 2, 'keys': []},
            {'number': 11, 'type': 2, 'keys': [2, 3, 4]},
            {'number': 12, 'type': 3, 'keys': []},
            {'number': 13, 'type': 1, 'keys': [1, 4, 1]},
            {'number': 14, 'type': 2, 'keys': [3]},
            {'number': 15, 'type': 2, 'keys': [3, 3]},
            {'number': 16, 'type': 4, 'keys': [2]},
            {'number': 17, 'type': 2, 'keys': []},
            {'number': 18, 'type': 1, 'keys': [1, 2, 1, 3, 2]},
            {'number': 19, 'type': 2, 'keys': [2, 3, 4]},
            {'number': 20, 'type': 4, 'keys': [2]},
        ]
    },
]


class TestTreasuryReader(TestCase):
    def test_reads_correctly_first_two_cases(self):
        with TreasuryReader(SMALL_INPUT_FILE) as reader:
            self.assertEqual(next(reader), CASES[0])
            self.assertDictEqual(next(reader), CASES[1])
    