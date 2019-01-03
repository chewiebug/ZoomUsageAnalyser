import argparse
from pathlib import Path


class CliArgs(object):
    """ Contains all properties parsed from cli """
    def __init__(self):
        self.__directory = 'missing'

    @property
    def get_directory(self):
        return self.__directory

    def __repr__(self):
        return type(self).__name__ + '(directory={})'.format(self.directory)


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description='Process a directory containing photos (jpg files).')
    parser.add_argument('-d', '--directory',
                        required=True,
                        help='relative or absolute path to directory containing photos')

    cli_args = CliArgs()
    return parser.parse_args(namespace=cli_args)


def traverse_directory(directory: str):
    p = Path(directory)
    if p.exists():
        print([x for x in p.glob('*.jpg') if not x.is_dir()])
    else:
        # TODO throw Exception?
        print('"' + directory + '" could not be found')


def main():
    cli_args = parse_args()
    print('arguments: ', cli_args)
    print('directory:', cli_args.directory)
    traverse_directory(cli_args.directory)


if __name__ == "__main__":
    main()
