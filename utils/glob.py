import os
import sys
import shutil
from pathlib import Path

from termcolor import colored


def get_cwd():
    return os.getcwd()


def join_path(*args):
    return os.path.join(*args)


def get_dirname(path):
    return os.path.dirname(path)


def is_abs(path):
    return os.path.isabs(path)


def get_abs_path(path):
    if path == ".":
        return get_cwd()

    path = os.path.normpath(path)
    path = path[1:] if path.startswith("\\") else path

    if not is_abs(path):
        path = join_path(get_cwd(), path)

    return path


def correct_path(path):
    path = path[1:-1] if path.startswith('"') and path.endswith('"') else path
    path = path[1:-1] if path.startswith('"') and path.endswith('"') else path

    path = os.path.normpath(path)

    path = path[1:] if path.startswith("\\") else path

    return path


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def get_file_name(file, type="name"):
    if type == "ext":
        return Path(file).suffix[1:]
    else:
        return Path(file).stem


def get_all_video_files(path):
    video_files = []
    video_extensions = [
        "mp4",
        "mkv",
        "avi",
        "mov",
        "m4a",
        "m4v",
        "mpg",
        "mpeg",
        "wmv",
        "webm",
        "flv",
    ]

    if os.path.isfile(path):
        video_files.append(Path(path))
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                extension = get_file_name(file, "ext").lower()
                if extension in video_extensions:
                    video_files.append(Path(root) / file)
    else:
        print(colored("Input path does not exist", "red"))
        return False

    return video_files
