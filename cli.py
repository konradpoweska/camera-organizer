import sys
from argparse import ArgumentParser

from app_logger import log
from config import Config


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=sys.argv[0], description="Organizes pictures by date")

    parser.add_argument("source_dir", nargs="+")
    parser.add_argument("destination_dir")
    parser.add_argument(
        "-s",
        "--subdirectory",
        metavar="NAME",
        help="e.g. 'Phone' will make files go to '2023/2023-10-12/Phone/'",
    )
    parser.add_argument("-m", "--by_month", action="store_true")
    parser.add_argument("-c", "--copy", action="store_true")
    parser.add_argument("-n", "--dry_run", action="store_true")
    parser.add_argument(
        "--logging",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    return parser


def parse_config() -> Config:
    args = get_parser().parse_args()

    if args.logging:
        log.setLevel(args.logging)

    return Config(
        source_dirs=args.source_dir,
        destination_dir=args.destination_dir,
        subdirectory=args.subdirectory,
        by_month=args.by_month,
        copy=args.copy,
        dry_run=args.dry_run,
    )
