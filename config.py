class Config:
    def __init__(
        self,
        source_dirs: list[str],
        destination_dir: str,
        subdirectory: str | None,
        by_month: bool = False,
        copy: bool = False,
        dry_run: bool = False,
    ):
        self.source_dirs = source_dirs
        self.destination_dir = destination_dir
        self.subdirectory = subdirectory
        self.by_month = by_month
        self.copy = copy
        self.dry_run = dry_run
