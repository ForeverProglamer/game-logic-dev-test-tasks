from pathlib import Path
from unittest import TestCase, skip

from core import Chest, Treasury, find_one_path_to_open_all_chests
from main import LARGE_INPUT_FILE, SMALL_INPUT_FILE
from utils import TreasuryReader


class TestCanOpenChestsFromFile(TestCase):
    def _test_opens_chests_from_file(self, path: Path):
        with TreasuryReader(path) as reader:
            for index, treasury in enumerate(reader, 1):
                solver = TreasureHunter(treasury)
                solution = find_one_path_to_open_all_chests(**treasury)
                can_solve = solver.can_open_all_chests(solution)
                
                with self.subTest(
                    msg=f'Case #{index}',
                    solution=solution,
                    can_solve=can_solve
                ):
                    self.assertEqual(can_solve, solution != [])

    def test_opens_chests_from_small_file(self):
        self._test_opens_chests_from_file(SMALL_INPUT_FILE)

    @skip('Takes 20 minutes to execute')
    def test_opens_chests_from_large_file(self):
        self._test_opens_chests_from_file(LARGE_INPUT_FILE)


class TreasureHunter:
    def __init__(self, treasury: Treasury) -> None:
        self._keys_pool = treasury['keys'].copy()
        self._chests = treasury['chests'].copy()
        self._opened_chests: list[int] = []

    def can_open_all_chests(self, solution: list[int]) -> bool:
        if len(solution) != len(self._chests):
            return False

        for chest_number in solution:
            if not self._open_chest(chest_number):
                return False

        return True

    def _open_chest(self, chest_number: int) -> bool:
        chest = self._find_chest_by_number(chest_number)
        
        if chest['type'] not in self._keys_pool:
            return False
        
        self._keys_pool.remove(chest['type'])
        self._keys_pool.extend(chest['keys'])
        self._opened_chests.append(chest_number)

        return True

    def _find_chest_by_number(self, chest_number: int) -> Chest:
        return next(filter(
            lambda c: c['number'] == chest_number, self._chests
        ))
