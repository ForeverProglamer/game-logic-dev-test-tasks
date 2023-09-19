from itertools import product


def shift_picture_to_frame_start(
    frame: list[list[int]],
    pic_width: int,
    pic_height: int,
    pic_x: int,
    pic_y: int
) -> None:
    """Shifts a picture's elements to the top left corner of a frame."""
    _validate_input(frame, pic_width, pic_height, pic_x, pic_y)
    
    if pic_width == 0 or pic_height == 0:
        return
    if pic_x == 0 and pic_y == 0:
        return
    
    for i, j in product(range(pic_height), range(pic_width)):
        k = i + pic_y
        h = j + pic_x
        frame[i][j], frame[k][h] = frame[k][h], frame[i][j]


def _validate_input(
    frame: list[list[int]],
    pic_width: int,
    pic_height: int,
    pic_x: int,
    pic_y: int
) -> None:
    if frame == [] or any(len(row) == [] for row in frame):
        raise ValueError('Cannot shift the picture within an empty frame')

    if pic_width < 0 or pic_height < 0 or pic_x < 0 or pic_y < 0:
        raise ValueError('Picture parameters cannot be negative values')

    frame_width = len(frame[0])
    frame_height = len(frame)
    
    if pic_x + pic_width > frame_width or pic_y + pic_height > frame_height:
        raise ValueError('The picture must be within the frame')
