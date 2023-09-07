from itertools import product


def shift_picture_to_frame_start(
    frame: list[list[int]],
    pic_width: int,
    pic_height: int,
    pic_x: int,
    pic_y: int
) -> None:
    """Shifts a picture's elements to the top left corner of a frame."""
    if pic_width == 0 or pic_height == 0:
        return
    if pic_x == 0 and pic_y == 0:
        return
    
    for i, j in product(range(pic_height), range(pic_width)):
        k = i + pic_y
        h = j + pic_x
        frame[i][j], frame[k][h] = frame[k][h], frame[i][j]
