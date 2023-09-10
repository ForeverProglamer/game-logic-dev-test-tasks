from collections import deque
from dataclasses import dataclass
from typing import TypedDict


class Chest(TypedDict):
    number: int
    type: int
    keys: list[int]


class Treasury(TypedDict):
    keys: list[int]
    chests: list[Chest]


@dataclass(frozen=True)
class _TreasuryState:
    keys_pool: list[int]
    opened_chests: list[int]

    def from_chest(self, chest: Chest) -> '_TreasuryState':
        keys_pool = self.keys_pool.copy() + chest['keys']
        keys_pool.remove(chest['type'])

        return _TreasuryState(
            keys_pool,
            self.opened_chests + [chest['number']]
        )


def find_one_path_to_open_all_chests(
    keys: list[int], chests: list[Chest]
) -> list[int]:
    """
    Returns lexicographically smallest path to open all chests in a treasury.
    """
    paths = find_all_paths_to_open_all_chests(keys, chests)
    if paths == []:
        return []
    return _get_lexicographically_smallest(paths)


def find_all_paths_to_open_all_chests(
    keys: list[int], chests: list[Chest]
) -> list[list[int]]:
    """Returns all possible paths to open all chests in a treasury."""
    total_chests = len(chests)
    results: list[list[int]] = []

    steps_to_take: deque[_TreasuryState] = deque([_TreasuryState(keys, [])])

    while steps_to_take:
        treasury = steps_to_take.popleft()
        closed_chests = _discover_closed_chests(treasury, chests)

        if closed_chests == [] and len(treasury.keys_pool) != 0 and len(treasury.opened_chests) < total_chests:
            # It's impossible to open all chests
            continue

        if closed_chests == [] and len(treasury.opened_chests) == total_chests:
            results.append(treasury.opened_chests)

        if closed_chests != []:
            steps_to_take.extend(_open_chests(closed_chests, treasury))

    return results


def _discover_closed_chests(
    treasury: _TreasuryState,
    chests: list[Chest],
) -> list[Chest]:
    def predicate(chest: Chest) -> bool:
        return (
            chest['type'] in treasury.keys_pool and
            chest['number'] not in treasury.opened_chests
        )
    
    return list(filter(predicate, chests))


def _open_chests(
    closed_chests: list[Chest],
    treasury: _TreasuryState
) -> list[_TreasuryState]:
    return [treasury.from_chest(chest) for chest in closed_chests]


def _get_lexicographically_smallest(paths: list[list[int]]) -> list[int]:
    strings = [','.join(map(str, path)) for path in paths]
    smallest = min(strings)
    return list(map(int, smallest.split(',')))
