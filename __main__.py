import cli
from lib import move_files

if __name__ == "__main__":
    config = cli.parse_config()
    move_files(config)
