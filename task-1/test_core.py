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
            shift_picture_to_frame_start(**item['input'])
            self.assertListEqual(
                item['input']['frame'], item['expected_result']
            )
