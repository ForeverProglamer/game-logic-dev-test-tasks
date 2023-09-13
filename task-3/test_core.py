from itertools import chain
from unittest import TestCase

from core import (
    _LazyQueue,
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
            with self.subTest(msg=f'Test {index}', treasury=treasury):
                self.assertListEqual(
                    list(find_all_paths_to_open_all_chests(**treasury)),
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
            with self.subTest(msg=f'Test {index}', treasury=treasury):
                self.assertListEqual(
                    find_one_path_to_open_all_chests(**treasury),
                    expected
                )


class TestLazyQueue(TestCase):
    def _to_gen(self, items):
        for item in items:
            yield item

    def test_popleft_raises_index_error_if_deque_is_empty(self):
        queue = _LazyQueue()
        with self.assertRaises(IndexError, msg='pop from an empty deque'):
            queue.popleft()

    def test_popleft_raises_index_error_if_empty_generator_passed(self):
        queue = _LazyQueue((0 for _ in range(0)))
        with self.assertRaises(IndexError, msg='pop from an empty lazy deque'):
            queue.popleft()

    def test_popleft_works_correctly_with_initialized_data(self):
        data = list(range(1, 11))
        queue = _LazyQueue(self._to_gen(data))

        for expected in data:
            self.assertEqual(queue.popleft(), expected)

    def test_append_works_correctly(self):
        gen = (i for i in range(1, 11))
        gen2 = (i for i in range(20, 31))
        queue = _LazyQueue()

        queue.append(gen)
        queue.append(gen2)

        self.assertListEqual(list(queue._deque), [gen, gen2])

    def test_complex_usage_1(self):
        lst = list(range(1, 11))
        lst2 = list(range(20, 31))

        queue = _LazyQueue(self._to_gen(lst))
        queue.append(self._to_gen(lst2))

        for expected in chain(lst, lst2):
            self.assertEqual(queue.popleft(), expected)

    def test_complex_usage_2(self):
        lst = list(range(1, 11))
        lst2 = list(range(20, 31))

        queue = _LazyQueue()
        queue.append(self._to_gen(lst))
        queue.append(self._to_gen(lst2))

        for expected in chain(lst, lst2):
            self.assertEqual(queue.popleft(), expected)
