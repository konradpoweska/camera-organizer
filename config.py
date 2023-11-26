class Config:
    def __init__(
        self,
        sources: list[str],
        destination_dir: str,
        subdirectory: str | None,
        by_month: bool = False,
        move: bool = False,
        dry_run: bool = False,
    ):
        self.sources = sources
        self.destination_dir = destination_dir
        self.subdirectory = subdirectory
        self.by_month = by_month
        self.move = move
        self.dry_run = dry_run
