import shutil
import subprocess
import os
import threading
import io
from subprocess import TimeoutExpired
from multiprocessing import Process, Queue

import time


def run_python(base_dir, timeout):
    queue = Queue()
    queue.put(bytearray("---------- MODULE STARTED  ----------\n", encoding='utf-8'))

    # Копируем файлы, которые были в прошлом запуске
    if len(os.listdir(os.path.join(base_dir, 'in'))) > 0:
        try:
            shutil.rmtree(os.path.join(base_dir, "in_old"))
        except FileNotFoundError:
            pass
        shutil.copytree(os.path.join(base_dir, 'in'), os.path.join(base_dir, "in_old"))
    # Запуск модуля в отдельном подпроцессе
    try:
        proc = subprocess.run(["python3", os.path.join(base_dir, 'start.py')], cwd=base_dir, timeout=timeout,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        queue.put(proc.stdout)
        with open(os.path.join(base_dir, "out.txt"), 'wb') as f:
            f.write(proc.stdout)
    except TimeoutExpired as e:
        queue.put(bytearray("Process has timed out after {} seconds\n".format(timeout), encoding='utf-8'))

    queue.put(bytearray("---------- MODULE FINISHED ----------\n", encoding='utf-8'))
    # Добавление в Log
    with open(os.path.join(base_dir, "log.txt"), 'ab') as f:
        while not queue.empty():
            f.write(queue.get())


def run_exe(base_dir):
    pass


if __name__ == '__main__':
    test_path = "/Users/ilya/Documents/PycharmProjects/Escort/modules/Test"
    test2_path = "/Users/ilya/Documents/PycharmProjects/Escort/modules/Test_2"
    test3_path = "/Users/ilya/Documents/PycharmProjects/Escort/modules/Top Kek"
    p = Process(target=
                run_python, args=(test2_path, 10))
    p.start()
    # threading.Thread(target=run_python, args=(test2_path, 0)).start()
    # for i in range(500):
    #     threading.Thread(target=run_python, args=(test2_path,)).start()
    # print("Done")
