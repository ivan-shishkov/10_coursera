import argparse


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'output',
        help='a xlsx file to save info about Coursera courses',
        type=str,
    )
    parser.add_argument(
        '--count',
        help='a count of randomly selected Coursera courses (default: 20)',
        default=20,
        type=int,
    )
    command_line_arguments = parser.parse_args()

    return command_line_arguments


def main():
    command_line_arguments = parse_command_line_arguments()

    output_filepath = command_line_arguments.output
    courses_count = command_line_arguments.count


if __name__ == '__main__':
    main()
