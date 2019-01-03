import argparse
import collections
from pathlib import Path
from typing import List

import exif_handler

CliArgs = collections.namedtuple('CliArgs', 'input_directory output_file')


def parse_args() -> CliArgs:
    parser = argparse.ArgumentParser(description='Process a directory containing photos (jpg files).')
    parser.add_argument('-id', '--input_directory',
                        required=True,
                        help='relative or absolute path to directory containing photos')
    parser.add_argument('-of', '--output_file',
                        required=True,
                        help='absolute path to file, where result should be written')
    parse_result = parser.parse_args()
    return CliArgs(parse_result.input_directory, parse_result.output_file)


def create_exifinfo_list(directory: str) -> List[exif_handler.ImageInfo]:
    p = Path(directory)
    if p.exists():
        exif_info_list = [exif_handler.get_zoom_value(jpgfile) for jpgfile in p.rglob('*.jpg') if not jpgfile.is_dir()]
        print('found {} files in {}'.format(len(exif_info_list), directory))
        return exif_info_list
    else:
        # TODO throw Exception?
        print('"' + directory + '" could not be found')


def main():
    cli_args = parse_args()
    print('arguments: ', cli_args)
    print('input directory:', cli_args.input_directory)

    exif_info_list = create_exifinfo_list(cli_args.input_directory)

    with open(cli_args.output_file, 'w') as f:
        f.write('filename;image_model;iso;focal_length;focal_length_35mm\n')
        for exif_info in exif_info_list:
            f.write(__exif_info_as_csv_line__(exif_info))

    print('{} lines written to {}:'.format(len(exif_info_list), cli_args.output_file))


def __exif_info_as_csv_line__(exif_info: exif_handler.ImageInfo):
    return '{};{};{};{};{}\n'.format(exif_info.filename,
                                     exif_info.image_model.value,
                                     exif_info.exif_iso_speed_ratings.value,
                                     exif_info.exif_focal_length.value,
                                     exif_info.exif_focal_length_in_35mm_film.value)


if __name__ == "__main__":
    main()
