import os
import re
import shutil
from datetime import datetime

from PIL import Image

from config import Config

SUPPORTED_EXTENTIONS = ["jpe?g", "arw", "cr2"]
SUPPORTED_EXTENTIONS_PATTERN = re.compile(
    rf"\.(?:{'|'.join(SUPPORTED_EXTENTIONS)})$", re.IGNORECASE
)
EXCLUDE_PATTERN = re.compile(r"\._|thumb|trash", re.IGNORECASE)


def move_files(config: Config):
    for source_dir in config.source_dirs:
        for root, _, files in os.walk(source_dir):
            if path_is_excluded(root):
                continue
            for file in files:
                if not file_is_wanted(file):
                    continue
                file_path = os.path.join(root, file)

                date_path = get_date_path(file_path, config.by_month)
                destination_path = get_destination_path(
                    config.destination_dir, date_path, config.subdirectory
                )
                os.makedirs(destination_path, exist_ok=True)
                shutil.move(file_path, destination_path)
                print(f"{file_path} -> {destination_path}")


def file_is_wanted(path: str) -> bool:
    return file_is_supported(path) and not path_is_excluded(path)


def file_is_supported(path: str) -> bool:
    return SUPPORTED_EXTENTIONS_PATTERN.search(path) is not None


def path_is_excluded(path: str) -> bool:
    return EXCLUDE_PATTERN.search(path) is not None


def get_date_path(file: str, by_month: bool) -> str:
    date = get_creation_time(file)
    year = str(date.year)
    if by_month:
        date = date.strftime("%Y-%m")
    else:
        date = date.strftime("%Y-%m-%d")
    destination_path = os.path.join(year, date)
    return destination_path


def get_destination_path(
    destination_dir: str, date_path: str, subfolder: str | None
) -> str:
    destination_path = os.path.join(destination_dir, date_path)
    if subfolder:
        destination_path = os.path.join(destination_path, subfolder)
    return destination_path


SONY_EXIF = 36867
CANON_EXIF = 306


def get_creation_time(file: str) -> datetime:
    time = get_creation_from_exif(file)
    if time is None:
        print(f"Time not found for {file}, using modified time")
        time = get_file_modified_date(file)
    return time


def get_creation_from_exif(file: str) -> datetime | None:
    im = Image.open(file)
    exif = im.getexif()
    creation_time: str | None = exif.get(SONY_EXIF) or exif.get(CANON_EXIF)
    if creation_time is None:
        return None
    return datetime.strptime(creation_time, "%Y:%m:%d %H:%M:%S")


def get_file_modified_date(file: str) -> datetime:
    modified_timestamp = os.path.getmtime(file)
    return datetime.fromtimestamp(modified_timestamp)
