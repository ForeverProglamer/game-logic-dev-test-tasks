import sys
from pathlib import Path

from core import find_one_path_to_open_all_chests
from utils import TreasuryReader

SMALL_INPUT_FILE = Path('Treasure_1_Small.in')
LARGE_INPUT_FILE = Path('Treasure_2_Large.in')

SMALL_OUTPUT_FILE = Path('Treasure_1_Small.out')
LARGE_OUTPUT_FILE = Path('Treasure_2_Large.out')

WRITE_MODE = 'w'


def main() -> None:
    process_input_file(SMALL_INPUT_FILE, SMALL_OUTPUT_FILE)
    process_input_file(LARGE_INPUT_FILE, LARGE_OUTPUT_FILE)
    
    print('Finished!')
    print(f'Check {SMALL_OUTPUT_FILE} and {LARGE_OUTPUT_FILE} for results')
    input('Press ENTER to exit...')


def process_input_file(input_file: Path, output_file: Path) -> None:
    print(f'Processing {input_file}...')
    
    with (
        TreasuryReader(input_file) as reader,
        open(output_file, WRITE_MODE) as writer
    ):
        for index, treasury in enumerate(reader, 1):
            print(f'Trying to open all chests for case #{index}...')
            result = find_one_path_to_open_all_chests(**treasury)
            writer.write(f'{prepare_result(index, result)}\n')


def prepare_result(index: int, path: list[int]) -> str:
    if path == []:
        return f'Case #{index}: IMPOSSIBLE'
    else:
        return f'Case #{index}: {" ".join(map(str, path))}'


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
