import os
from typing import Dict


def create_files(files: Dict[str, str]):
    for file, content in files.items():
        with open(file, 'w') as f:
            f.write(content)


def delete_files(files: Dict[str, str]):
    for file in files.keys():
        if os.path.isfile(file):
            os.remove(file)
