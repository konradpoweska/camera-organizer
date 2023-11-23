import os
import re
from datetime import datetime


def get_file_extension_pattern(extensions: list[str]) -> re.Pattern:
    return re.compile(rf"\.(?:{'|'.join(extensions)})$", re.IGNORECASE)


def get_file_modified_date(file: str) -> datetime:
    modified_timestamp = os.path.getmtime(file)
    return datetime.fromtimestamp(modified_timestamp)
