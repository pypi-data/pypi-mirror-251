import argparse
from typing import List, Dict

from grepy.grep import grep_recursive_m, grep_count, grep_m, MatchResults


def main():
    parser = argparse.ArgumentParser(description='''
            A grep-like command-line utility from LiteRank,
            see https://literank.com/project/9/intro''')
    parser.add_argument('pattern', type=str, help='The pattern to search for')
    parser.add_argument('file_paths', nargs="*", default=[],
                        help='File paths to search in')

    # Optional arguments
    parser.add_argument('-c', '--count', action='store_true',
                        help='Only a count of selected lines is written to \
                            standard output.')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='Perform case insensitive matching. By default, \
                            it is case sensitive.')
    parser.add_argument('-n', '--line-number', action='store_true',
                        help='Each output line is preceded by its relative \
                        line number in the file, starting at line 1. This \
                            option is ignored if -c is specified.')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='Recursively search subdirectories listed.')
    parser.add_argument('-v', '--invert-match', action='store_true',
                        help='Selected lines are those not matching any of \
                          the specified patterns.')

    args = parser.parse_args()

    if args.recursive and args.file_paths != "":
        result = grep_recursive_m(args.pattern,
                                  args.file_paths, get_options(args))
    else:
        result = grep_m(args.pattern, args.file_paths, get_options(args))

    if args.count:
        print(grep_count(result))
    else:
        print_result(result, args.line_number)


def get_options(args: argparse.Namespace) -> List[str]:
    options = []
    if args.ignore_case:
        options.append('i')
    if args.invert_match:
        options.append('v')
    return options


def print_result(result: Dict[str, MatchResults], line_number_option: bool):
    current_file = None
    file_count = len(result)
    for file_path, lines in result.items():
        for (line_number, line) in lines:
            if file_count > 1 and file_path != current_file:
                current_file = file_path
                print(f"\n{file_path}:")
            if line_number_option:
                print(f"{line_number}: {line}")
            else:
                print(line)


if __name__ == '__main__':
    main()
