import collections
import argparse
from functools import lru_cache


@lru_cache(maxsize=32)
def numberOfCharacters(str):
    count_char = collections.Counter(str)
    uniq_char = sum(1 for key, value in count_char.items() if value == 1)
    return uniq_char


def process_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--string")
    parser.add_argument("--file")
    args = parser.parse_args()
    if (args.file):
        file_content = process_file(args.file)
        print(numberOfCharacters(file_content))
    elif (args.string):
        print(numberOfCharacters(args.string))
