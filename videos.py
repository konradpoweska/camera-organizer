from datetime import datetime

from pymediainfo import MediaInfo

from common import get_file_extension_pattern

SUPPORTED_EXTENTIONS = ["mp4", "mts", "mov"]
VIDEO_FILE_PATTERN = get_file_extension_pattern(SUPPORTED_EXTENTIONS)


def get_video_creation_time(path: str) -> datetime | None:
    media_info = MediaInfo.parse(path)
    assert isinstance(media_info, MediaInfo)

    track = media_info.general_tracks[0]
    recorded_date = track.recorded_date
    if recorded_date is None:
        return None
    return datetime.strptime(recorded_date, "%Y-%m-%d %H:%M:%S%z")
