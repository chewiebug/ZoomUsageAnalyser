import argparse
import collections
from pathlib import Path

import exif_handler

CliArgs = collections.namedtuple('CliArgs', 'directory')


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description='Process a directory containing photos (jpg files).')
    parser.add_argument('-d', '--directory',
                        required=True,
                        help='relative or absolute path to directory containing photos')
    parse_result = parser.parse_args()
    return CliArgs(parse_result.directory)


def traverse_directory(directory: str):
    p = Path(directory)
    if p.exists():
        jpgfiles = [x for x in p.glob('*.jpg') if not x.is_dir()]
        print('found {} files in {}'.format(len(jpgfiles), directory))
        for jpgfile in jpgfiles:
            print('tags of {}: {}'.format(jpgfile, exif_handler.get_zoom_value(jpgfile)))
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
