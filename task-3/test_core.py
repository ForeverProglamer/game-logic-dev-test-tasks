from typing import TypedDict
from unittest import TestCase

from core import (
    Treasury,
    find_all_paths_to_open_all_chests,
    find_one_path_to_open_all_chests
)


class TestOpenAllChests(TestCase):
    def setUp(self) -> None:
        self.treasuries: list[Treasury] = [
           {
               'keys': [1],
               'chests': [
                   {'number': 1, 'type': 1, 'keys': []},
                   {'number': 2, 'type': 1, 'keys': [1, 3]},
                   {'number': 3, 'type': 2, 'keys': []},
                   {'number': 4, 'type': 3, 'keys': [2]}
                ]
            },
            {
               'keys': [1, 1, 1],
               'chests': [
                   {'number': 1, 'type': 1, 'keys': []},
                   {'number': 2, 'type': 1, 'keys': []},
                   {'number': 3, 'type': 1, 'keys': []},
                ]
            },
            {
               'keys': [2],
               'chests': [
                   {'number': 1, 'type': 1, 'keys': [1]},
                ]
            }
        ]

    def test_finds_all_possible_paths_to_open_all_chests(self):
        expected_results: list[list[list[int]]] = [
            [[2, 1, 4, 3], [2, 4, 1, 3], [2, 4, 3, 1]],
            [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]],
            []
        ]

        results_iter = iter(expected_results)
        for index, treasury in enumerate(self.treasuries, 0):
            expected = next(results_iter)
            with self.subTest(msh=f'Test {index}', treasury=treasury):
                self.assertListEqual(
                    find_all_paths_to_open_all_chests(**treasury),
                    expected
                )

    def test_find_lexicographically_smallest_path_to_open_all_chests(self):
        expected_results = [
            [2, 1, 4, 3],
            [1, 2, 3],
            []
        ]

        results_iter = iter(expected_results)
        for index, treasury in enumerate(self.treasuries, 0):
            expected = next(results_iter)
            with self.subTest(msh=f'Test {index}', treasury=treasury):
                self.assertListEqual(
                    find_one_path_to_open_all_chests(**treasury),
                    expected
                )