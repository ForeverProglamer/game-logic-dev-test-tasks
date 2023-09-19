import sys

from core import dollars_to_english_text


def main() -> None:
    while True:
        try:
            number = float(input('Enter a number (e.g. 56789.99): '))
            result = dollars_to_english_text(number)
            print(result)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            sys.exit()


if __name__ == '__main__':
    main()
