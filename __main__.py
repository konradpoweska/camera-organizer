import cli
from lib import organize_camera

if __name__ == "__main__":
    config = cli.parse_config()
    organize_camera(config)
