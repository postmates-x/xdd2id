import argparse
from . import convert


def main():
    """ CANopen XML dictionary to Ingenia dictionary converter tool. """

    parser = argparse.ArgumentParser(
        description=('CANopen XML dictionary to Ingenia dictionary converter '
                     'tool'))
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='XDD file')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='IngeniaDictionary file')

    args = parser.parse_args()

    convert(args.input, args.output)


if __name__ == '__main__':
    main()
