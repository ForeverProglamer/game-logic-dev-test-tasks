from functools import partial
from typing import Union

MIN_NUMBER = 0
MAX_NUMBER = 1_000_000_000

CENT_PART_MAX_LENGTH = 2

DOLLAR = 'dollar'
CENT = 'cent'

DIGITS = {
    '0': '',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine'
}

TEENS = {
    '10': 'ten',
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'nineteen',
}

TENS = {
    '2': 'twenty',
    '3': 'thirty',
    '4': 'forty',
    '5': 'fifty',
    '6': 'sixty',
    '7': 'seventy',
    '8': 'eighty',
    '9': 'ninety'
}

MAGNITUDES = {
    0: '',
    1: 'thousand',
    2: 'million',
    3: 'billion'
}

NUMBER_SEPARATOR = '.'

SHORT_TENS_NOTATION_LENGTH = 1

TRIPLET_TO_SKIP = '000'

ONE_DIGIT_NUMBER_LENGTH = 1
TWO_DIGIT_NUMBER_LENGTH = 2
THREE_DIGIT_NUMBER_LENGTH = 3

ZERO = '0'
ONE = '1'

STOP = -1
STEP = 3


def dollars_to_english_text(number: Union[float, int]) -> str:
    """
    Takes a number of dollars and cents, 
    and represents it as an English text.
    """
    number = float(number)

    _validate_input(number)
    
    dollar_part, cent_part = _separate_number_parts(number)

    dollars_number = _get_dollars_number_from(dollar_part)
    cents_number = _get_cents_number_from(cent_part)

    dollars_text = _prepare_dollars_text(dollars_number)
    cents_text = _prepare_cents_text(cents_number)

    return f'{dollars_text} {cents_text}'.strip()


def _validate_input(number: float) -> None:
    if number > MAX_NUMBER or number <= MIN_NUMBER:
        raise ValueError('Given value is out of allowed range')
    
    _, cent_part = str(number).split(NUMBER_SEPARATOR)

    if len(cent_part) > CENT_PART_MAX_LENGTH:
        raise ValueError('Cent part must be less than 3 digits')


def _separate_number_parts(number: float) -> tuple[str, str]:
    dollar_part, cent_part = str(number).split(NUMBER_SEPARATOR)

    if len(cent_part) == SHORT_TENS_NOTATION_LENGTH:
        cent_part = f'{cent_part}0'

    return dollar_part, cent_part


def _get_dollars_number_from(dollar_part: str) -> str:
    triplets = _get_number_triplets_from(dollar_part)

    result = ''
    for index, triplet in enumerate(triplets):
        if triplet == TRIPLET_TO_SKIP:
            continue
        result = f'{_map_number_to_text(triplet)} {MAGNITUDES[index]} {result}'
    return result


def _get_cents_number_from(cent_part: str) -> str:
    return _map_number_to_text(cent_part)


def _get_number_triplets_from(number: str) -> list[str]:
    triplets = []

    for i in range(len(number), STOP, -STEP):
        triplet = ''.join([number[j] for j in range(i-STEP, i) if j >= 0])
        if triplet != '':
            triplets.append(triplet)

    return triplets


def _map_number_to_text(triplet: str) -> str:
    length = len(triplet)
    if length == ONE_DIGIT_NUMBER_LENGTH:
        return _map_one_digit_number(triplet[0])
    elif length == TWO_DIGIT_NUMBER_LENGTH:
        return _map_two_digit_number(triplet[:2])
    elif length == THREE_DIGIT_NUMBER_LENGTH:
        return _map_three_digit_number(triplet)
    return ''


def _map_one_digit_number(number: str) -> str:
    return DIGITS[number]


def _map_two_digit_number(number: str) -> str:
    if number[0] == ZERO:
        return _map_one_digit_number(number[1])

    if number[0] == ONE:
        return TEENS[number]
    
    result = TENS[number[0]]

    if number[1] == ZERO:
        return result
    
    return f'{result}-{_map_one_digit_number(number[1])}'


def _map_three_digit_number(number: str) -> str:
    if number[0] == ZERO:
        return _map_two_digit_number(number[1:3])
    
    result = f'{_map_one_digit_number(number[0])} hundred'
    
    if number[2] == ZERO and number[1] == ZERO:
        return result

    if number[1] == ZERO:
        return f'{result} {_map_one_digit_number(number[2])}'

    return f'{result} {_map_two_digit_number(number[1:3])}'


def _prepare_dollars_text(number: str) -> str:
    number = number.strip()
    if not number:
        return ''
    return f'{number} {_get_dollar_text(plural=number != DIGITS[ONE])}'


def _prepare_cents_text(number: str) -> str:
    number = number.strip()
    if not number:
        return ''
    return f'{number} {_get_cent_text(plural=number != DIGITS[ONE])}'


def _get_correct_form(word: str, plural: bool) -> str:
    return f'{word}s' if plural else word


_get_dollar_text = partial(_get_correct_form, word=DOLLAR)
_get_cent_text = partial(_get_correct_form, word=CENT)
