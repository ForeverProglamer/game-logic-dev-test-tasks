from collections import Iterator
from contextlib import AbstractContextManager
from pathlib import Path
from types import TracebackType
from typing import Optional

from core import Treasury


class TreasuryReader(Iterator, AbstractContextManager):
    def __init__(self, path: Path) -> None:
        self._path = path
    
    def __enter__(self) -> 'TreasuryReader':
        self._file = self._path.open()
        self._cases_number = int(self._file.readline())
        return self

    def __next__(self) -> Treasury:
        try:
            _, number_of_chests = list(map(int, self._file.readline().split(' ')))
        except ValueError:
            raise StopIteration()
        
        keys_pool = list(map(int, self._file.readline().split(' ')))
        chests = []
        
        for i in range(number_of_chests):
            key_type, _, *keys = list(map(
                int, self._file.readline().split(' '))
            )
            chests.append({'number': i+1, 'type': key_type, 'keys': keys})
        
        return {
            'keys': keys_pool,
            'chests': chests
        }

    def __exit__(
        self,
        __exc_type: Optional[type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        if self._file:
            self._file.close()
