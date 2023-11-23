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
                time = try_get_creation_time(file_path)

                if time is None:
                    log.debug('Ignoring file "%s" (not included)', file)
                else:
                    move_file(config, file_path, time)

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


def move_file(config: Config, file: str, time: datetime):
    date_path = get_date_path(time, config.by_month)
    destination_path = get_destination_path(
        config.destination_dir, date_path, config.subdirectory
    )
    if not config.dry_run:
        os.makedirs(destination_path, exist_ok=True)
        if config.copy:
            shutil.copy(file, destination_path)
        else:
            shutil.move(file, destination_path)
    log.info("%s -> %s", file, destination_path)


def get_date_path(time: datetime, by_month: bool) -> str:
    year = str(time.year)
    if by_month:
        date = time.strftime("%Y-%m")
    else:
        date = time.strftime("%Y-%m-%d")
    destination_path = os.path.join(year, date)
    return destination_path


def get_destination_path(
    destination_dir: str, date_path: str, subfolder: str | None
) -> str:
    destination_path = os.path.join(destination_dir, date_path)
    if subfolder:
        destination_path = os.path.join(destination_path, subfolder)
    return destination_path
