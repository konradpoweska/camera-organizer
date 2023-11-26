# Camera organizer

Import your media and organize them automatically by date.
Automatically scans a directory, finds pictures and videos, reads their date of creation from metadata, and moves them in a folder like `2023/2023-10-21`.

### Installation

```sh
# Create a virtual env
python -m venv venv

# Activate the virtual env (resets if shell is closed)
. venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

### Example

```console
$ python . /mnt/sdcard ~/Pictures
[INFO] "/mnt/sdcard/DCIM/100CANON/IMG_9948.JPG" -> "/home/konrad/Pictures/2023/2023-10-09/IMG_9948.JPG"
[INFO] "/mnt/sdcard/DCIM/100CANON/IMG_9949.JPG" -> "/home/konrad/Pictures/2023/2023-10-09/IMG_9949.JPG"
[INFO] "/mnt/sdcard/DCIM/100CANON/IMG_9950.JPG" -> "/home/konrad/Pictures/2023/2023-10-09/IMG_9950.JPG"
[INFO] "/mnt/sdcard/DCIM/100CANON/IMG_9955.JPG" -> "/home/konrad/Pictures/2023/2023-10-10/IMG_9955.JPG"
[INFO] "/mnt/sdcard/DCIM/100CANON/IMG_9956.JPG" -> "/home/konrad/Pictures/2023/2023-10-10/IMG_9956.JPG"
```

### Usage

```console
$ python . -h
usage: . [-h] [-s NAME] [--by_month] [-m] [-n]
         [--logging {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
         source_dir [source_dir ...] destination_dir

Import your media and organize them automatically by date.

positional arguments:
  source_dir
  destination_dir

options:
  -h, --help            show this help message and exit
  -s NAME, --subdirectory NAME
                        e.g. 'Phone' will make files go to '2023/2023-10-12/Phone/'
  --by_month            Group by month instead of by day.
  -m, --move            Move instead of copying.
  -n, --dry_run         Do not perform any actual actions on the files.
  --logging {DEBUG,INFO,WARNING,ERROR,CRITICAL}
```
