import collections
from pathlib import Path

import exifread

ExifKeyMapping = collections.namedtuple('ExifKeyMapping', ['exif_key', 'python_key', 'type'])
ExifElement = collections.namedtuple('ExifElement', ['exif_key', 'value', 'type'])

IMAGE_MODEL = ExifKeyMapping('Image Model', 'image_model', str)
EXIF_ISO_SPEED_RATINGS = ExifKeyMapping('EXIF ISOSpeedRatings', 'exif_iso_speed_ratings', int)
EXIF_FOCAL_LENGTH = ExifKeyMapping('EXIF FocalLength', 'exif_focal_length', str)
EXIF_FOCAL_LENGTH_IN_35MM_FILM = ExifKeyMapping('EXIF FocalLengthIn35mmFilm', 'exif_focal_length_in_35mm_film', int)

ImageInfo = collections.namedtuple('ImageInfo', [
    'filename',
    IMAGE_MODEL.python_key,
    EXIF_ISO_SPEED_RATINGS.python_key,
    EXIF_FOCAL_LENGTH.python_key,
    EXIF_FOCAL_LENGTH_IN_35MM_FILM.python_key,
    ])


def get_zoom_value(jpgfile: Path):
    tags = __get_exif_tags__(jpgfile)
    return ImageInfo(
        jpgfile.absolute(),
        __create_exif_element__(tags, IMAGE_MODEL),
        __create_exif_element__(tags, EXIF_ISO_SPEED_RATINGS),
        __create_exif_element__(tags, EXIF_FOCAL_LENGTH),
        __create_exif_element__(tags, EXIF_FOCAL_LENGTH_IN_35MM_FILM)
    )


def __create_exif_element__(tags: dict, key: ExifKeyMapping) -> ExifElement:
    return ExifElement(
        exif_key=key.exif_key,
        value=key.type(tags.get(key.exif_key).printable) if key.exif_key in tags.keys() else None,
        type=key.type,
    )


def __get_exif_tags__(jpgfile: Path):
    with jpgfile.open(mode='rb') as f:
        # Return Exif tags
        return exifread.process_file(f, details=False, strict=True)
