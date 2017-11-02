import os
from time import sleep

from .settings import *


def move_file(filename, path_for):
    os.rename(os.path.abspath(os.path.join(LISTEN_DIR, filename)),
              os.path.abspath(os.path.join(path_for, filename)))  # use shutil


def listen():
    global move_file
    while True:
        moved = 0
        for file in os.listdir(LISTEN_DIR):
            extension = file.split('.')[-1].lower()
            if extension == 'txt':
                move_file(file, PATH_FOR_TXT)
            elif extension == 'm':
                move_file(file, PATH_FOR_MATLAB)
            elif extension == 'exe':
                move_file(file, PATH_FOR_EXE)
            elif extension == 'py':
                move_file(file, PATH_FOR_PYTHON)
            elif extension in IMG_EXTENSIONS:
                move_file(file, PATH_FOR_MUSIC)
            elif extension in MUSIC_EXTENSIONS:
                move_file(file, PATH_FOR_MUSIC)
            else:
                # TODO add to log file
                print("Unexpected extension {} at file {}".format(extension, file))
                moved -= 1
            moved += 1
        if moved:
            print("Moved {} files".format(moved))
            moved = 0
        else:
            print("No files in directory")
        sleep(TIME_TO_LISTEN)


if __name__ == '__main__':
    listen()
