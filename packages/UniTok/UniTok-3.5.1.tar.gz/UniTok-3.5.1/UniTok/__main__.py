import argparse

from UniTok import UniDep


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', type=str, default='.', help='Path to the UniDep dataset')

    args = parser.parse_args()
    path = args.path

    depot = UniDep(path)
    print(depot)
