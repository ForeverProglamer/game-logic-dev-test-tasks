import json
from typing import TypedDict
from unittest import TestCase

from core import shift_picture_to_frame_start

TEST_DATA_FILENAME = 'test-data.json'


class FunctionInput(TypedDict):
    frame: list[list[int]]
    pic_width: int
    pic_height: int
    pic_x: int
    pic_y: int


class TestData(TypedDict):
    test_info: str
    input: FunctionInput
    expected_result: list[list[int]]


class ShiftPictureToFrameStart(TestCase):
    def setUp(self) -> None:
        with open(TEST_DATA_FILENAME) as f:
            self.data: list[TestData] = json.load(f)
    
    def test(self):
        for item in self.data:
            with self.subTest(item=item):
                shift_picture_to_frame_start(**item['input'])
                self.assertListEqual(
                    item['input']['frame'], item['expected_result']
                )

    def test_raises_value_error_when_frame_is_empty(self):
        frame = []
        pic_width = 1
        pic_height = 1
        pic_x = 1
        pic_y = 1

        with self.assertRaises(ValueError):
            shift_picture_to_frame_start(frame, pic_width, pic_height, pic_x, pic_y)
    
    def test_raises_value_error_when_picture_is_out_of_frame(self):
        frame = [[1, 2], [3, 4]]
        bad_inputs = [
            {'pic_width': 3, 'pic_height': 1, 'pic_x': 1, 'pic_y': 1},
            {'pic_width': 1, 'pic_height': 2, 'pic_x': 1, 'pic_y': 1},
            {'pic_width': 1, 'pic_height': 1, 'pic_x': 3, 'pic_y': 1},
            {'pic_width': 1, 'pic_height': 1, 'pic_x': 1, 'pic_y': 3},
            {'pic_width': -1, 'pic_height': 1, 'pic_x': 1, 'pic_y': 1},
            {'pic_width': 1, 'pic_height': -1, 'pic_x': 1, 'pic_y': 1},
            {'pic_width': 1, 'pic_height': 1, 'pic_x': -1, 'pic_y': 1},
            {'pic_width': 1, 'pic_height': 1, 'pic_x': 1, 'pic_y': -1},
        ]

        for inpt in bad_inputs:
            with (self.subTest(inpt=inpt), self.assertRaises(ValueError)):
                shift_picture_to_frame_start(frame, **inpt)
