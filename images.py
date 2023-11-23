from datetime import datetime

from PIL import Image

from common import get_file_extension_pattern

SUPPORTED_EXTENTIONS = ["jpe?g", "arw", "cr2"]
IMAGE_FILE_PATTERN = get_file_extension_pattern(SUPPORTED_EXTENTIONS)

SONY_EXIF = 36867
CANON_EXIF = 306


def get_image_creation_time(file: str) -> datetime | None:
    try:
        im = Image.open(file)
        exif = im.getexif()
        creation_time: str | None = exif.get(SONY_EXIF) or exif.get(CANON_EXIF)
    except Exception:
        creation_time = None

    if creation_time is None:
        return None
    return datetime.strptime(creation_time, "%Y:%m:%d %H:%M:%S")
