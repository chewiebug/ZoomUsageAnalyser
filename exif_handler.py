import exifread


def get_zoom_value(jpgfile: str):
    tags = __get_exif_tags__(jpgfile)
    print('tags:', tags)
    return tags


def __get_exif_tags__(jpgfile: str):
    with open(jpgfile, 'rb') as f:
        # Return Exif tags
        return exifread.process_file(f)
