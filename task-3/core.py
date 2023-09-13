from collections import deque
from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, Optional, TypeVar, TypedDict

QUEUE_MAX_LENGTH = 50

T = TypeVar('T')


class Chest(TypedDict):
    number: int
    type: int
    keys: list[int]


class Treasury(TypedDict):
    keys: list[int]
    chests: list[Chest]


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
) -> Iterator[list[int]]:
    """Returns all possible paths to open all chests in a treasury."""
    total_chests = len(chests)
    steps_to_take = _LazyQueue(_to_gen(_TreasuryState(keys, [])))

    while True:
        try:
            treasury = steps_to_take.popleft()
        except IndexError:
            break

        closed_chests = _discover_closed_chests(treasury, chests)

        if closed_chests == [] and len(treasury.opened_chests) == total_chests:
            # print(treasury.opened_chests)
            yield treasury.opened_chests

        if closed_chests != [] and len(steps_to_take) <= QUEUE_MAX_LENGTH:
            steps_to_take.append(_open_chests(closed_chests, treasury))


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


class _LazyQueue(Generic[T]):
    def __init__(self, items: Optional[Iterator[T]] = None) -> None:
        self._deque: deque[Iterator[T]] = deque()
        self._current_gen: Optional[Iterator[T]] = None

        if items is not None:
            self._current_gen = items
    
    def popleft(self) -> T:
        if self._current_gen is None:
            self._current_gen = self._deque.popleft()
            try:
                return next(self._current_gen)
            except StopIteration:
                self._current_gen = None
                raise IndexError('pop from an empty lazy deque')
        try:
            return next(self._current_gen)
        except StopIteration:
            self._current_gen = None
            return self.popleft()

    def append(self, items: Iterator[T]) -> None:
        self._deque.append(items)

    def __len__(self) -> int:
        return len(self._deque)


def _to_gen(item: T) -> Iterator[T]:
    yield item


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
    closed_chests: Iterable[Chest],
    treasury: _TreasuryState
) -> Iterator[_TreasuryState]:
    return (treasury.from_chest(chest) for chest in closed_chests)


def _get_lexicographically_smallest(paths: Iterable[list[int]]) -> list[int]:
    strings = [','.join(map(str, path)) for path in paths]
    if strings == []:
        return []
    smallest = min(strings)
    return list(map(int, smallest.split(',')))
