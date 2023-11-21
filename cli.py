import argparse
import sys

from config import Config

parser = argparse.ArgumentParser(
    prog=sys.argv[0], description="Organizes pictures by date"
)
parser.add_argument("source_dir", nargs="+")
parser.add_argument("destination_dir")
parser.add_argument(
    "-s",
    "--subdirectory",
    metavar="NAME",
    help="e.g. 'Phone' will make files go to '2023/2023-10-12/Phone/'",
)
parser.add_argument("-m", "--by_month", action="store_true")


def parse_config() -> Config:
    args = parser.parse_args()
    return Config(
        source_dirs=args.source_dir,
        destination_dir=args.destination_dir,
        subdirectory=args.subdirectory,
        by_month=args.by_month,
    )
