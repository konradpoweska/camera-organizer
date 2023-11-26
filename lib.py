import os
import re
import shutil
from datetime import datetime
from typing import Callable, Tuple

from app_logger import log
from common import get_file_modified_date
from config import Config
from images import IMAGE_FILE_PATTERN, get_image_creation_time
from videos import VIDEO_FILE_PATTERN, get_video_creation_time

EXCLUDE_PATTERN = re.compile(r"\._|thumb|trash", re.IGNORECASE)


def move_files(config: Config):
    assert os.path.isdir(
        config.destination_dir
    ), "Provided destination is not a directory"

    for source_dir in config.source_dirs:
        for root, _, files in os.walk(source_dir):
            if EXCLUDE_PATTERN.search(root):
                log.debug('Ignoring directory "%s" (excluded).', root)
                continue
            for file in files:
                if EXCLUDE_PATTERN.search(file):
                    log.debug('Ignoring file "%s" (excluded).', file)
                    continue

                file_path = os.path.join(root, file)
                try_move_file(config, file_path)

    if config.dry_run:
        log.info("(DRY-RUN)")


HANDLERS: list[Tuple[re.Pattern, Callable[[str], datetime | None]]] = [
    (IMAGE_FILE_PATTERN, get_image_creation_time),
    (VIDEO_FILE_PATTERN, get_video_creation_time),
]


def try_get_creation_time(file: str) -> datetime | None:
    for pattern, get_time in HANDLERS:
        if pattern.search(file):
            time = get_time(file)

            if time is None:
                log.warn(
                    "Could not determine creation time for '%s', falling back to file modified-time.",
                    file,
                )
                time = get_file_modified_date(file)

            return time
    return None


def try_move_file(config: Config, file: str):
    time = try_get_creation_time(file)
    if time is None:
        log.debug('Ignoring "%s" (file not detected as relevant)', file)
        return

    destination_path = get_destination_path(config, file, time)
    if os.path.exists(destination_path):
        log.info('Ignoring "%s" ("%s" already exists)', file, destination_path)
        return

    log.info('"%s" -> "%s"', file, destination_path)

    if not config.dry_run:
        os.makedirs(destination_path, exist_ok=True)
        if config.copy:
            shutil.copy(file, destination_path)
        else:
            shutil.move(file, destination_path)


def get_destination_path(config: Config, file: str, time: datetime) -> str:
    date_path = get_date_path(time, config.by_month)
    destination_path = os.path.join(config.destination_dir, date_path)
    if config.subdirectory:
        destination_path = os.path.join(destination_path, config.subdirectory)
    return os.path.join(destination_path, os.path.basename(file))


def get_date_path(time: datetime, by_month: bool) -> str:
    year = str(time.year)
    if by_month:
        date = time.strftime("%Y-%m")
    else:
        date = time.strftime("%Y-%m-%d")
    destination_path = os.path.join(year, date)
    return destination_path
