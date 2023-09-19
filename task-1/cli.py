import sys
from random import randint

from core import shift_picture_to_frame_start

MIN_VALUE_TO_GENERATE = 0
MAX_VALUE_TO_GENERATE = 101


def main() -> None:
    while True:
        action = input('Choose an action (0 - exit, 1 - run the function): ')
        try:
            action_handlers[action]()
        except KeyError:
            print('Unsupported action provided')
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            sys.exit()


def run_picture_shifting() -> None:
    raw_frame_size = input('Enter frame size (e.g. 4x4): ')
    cols, rows = parse_pair_of_ints(raw_frame_size, 'x')

    frame = generate_random_frame(cols, rows)

    print('Generated frame:')
    print_2d_array(frame)

    raw_picture_size = input('Enter picture size (e.g. 2x2): ')
    pic_width, pic_height = parse_pair_of_ints(raw_picture_size, 'x')

    raw_picture_coords = input('Enter picture start coordinates (e.g. 1,1): ')
    pic_x, pic_y = parse_pair_of_ints(raw_picture_coords, ',')

    shift_picture_to_frame_start(
        frame, pic_width, pic_height, pic_x, pic_y
    )

    print('Resulting frame:')
    print_2d_array(frame)


def parse_pair_of_ints(raw_size: str, separator: str) -> tuple[int, int]:
    x, y = raw_size.lower().strip().split(separator)
    return int(x), int(y)


def generate_random_frame(cols: int, rows: int) -> list[list[int]]:
    result = []
    for _ in range(rows):
        result.append([
            randint(MIN_VALUE_TO_GENERATE, MAX_VALUE_TO_GENERATE)
            for _ in range(cols)
        ])
    return result


def print_2d_array(array: list[list[int]]) -> None:
    for i in range(len(array)):
        for j in range(len(array[i])):
            print(
                f'{array[i][j]:{len(str(MAX_VALUE_TO_GENERATE))+1}}',
                end=' '
            )
        print()


action_handlers = {
    '0': sys.exit,
    '1': run_picture_shifting
}
