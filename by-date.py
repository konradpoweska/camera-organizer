#!/bin/env python

import os
import sys
import shutil
from datetime import datetime


def move_files(source_folder, destination_folder, subfolder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            modified_date = datetime.fromtimestamp(os.path.getmtime(file_path))
            year = str(modified_date.year)
            year_month = modified_date.strftime("%Y-%m")
            destination_path = os.path.join(
                destination_folder, year, year_month)
            if subfolder:
                destination_path = os.path.join(destination_path, subfolder)

            os.makedirs(destination_path, exist_ok=True)
            shutil.move(file_path, destination_path)
            print(f'{file_path} -> {destination_path}')


# Example usage:
source_folder = sys.argv[1]
destination_folder = sys.argv[2]
subfolder = sys.argv[3]

if __name__ == '__main__':
    move_files(source_folder, destination_folder, subfolder)
