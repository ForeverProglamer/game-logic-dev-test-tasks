import sys

from core import shift_picture_to_frame_start


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
    raw_frame_size = input('Enter frame size (ex. 4x4): ')
    rows, cols = parse_pair_of_ints(raw_frame_size, 'x')

    frame = [[] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            frame[i].append(int(input(f'Enter frame[{i}][{j}]: ')))

    print('Given frame:')
    print_2d_array(frame)

    raw_picture_size = input('Enter picture size (ex. 2x2): ')
    pic_width, pic_height = parse_pair_of_ints(raw_picture_size, 'x')

    raw_picture_coords = input('Enter picture start coordinates (ex. 1,1): ')
    pic_x, pic_y = parse_pair_of_ints(raw_picture_coords, ',')

    shift_picture_to_frame_start(
        frame, pic_width, pic_height, pic_x, pic_y
    )

    print('Resulting frame:')
    print_2d_array(frame)


def parse_pair_of_ints(raw_size: str, separator: str) -> tuple[int, int]:
    x, y = raw_size.lower().strip().split(separator)
    return int(x), int(y)


def print_2d_array(array: list[list[int]]) -> None:
    for i in range(len(array)):
        for j in range(len(array[i])):
            print(array[i][j], end=' ')
        print()


action_handlers = {
    '0': sys.exit,
    '1': run_picture_shifting
}
