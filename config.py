class Config:
    def __init__(
        self,
        source_dirs: list[str],
        destination_dir: str,
        subdirectory: str | None,
        by_month: bool,
    ):
        self.source_dirs: list[str] = source_dirs
        self.destination_dir: str = destination_dir
        self.subdirectory: str | None = subdirectory
        self.by_month: bool = by_month
