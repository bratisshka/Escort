import subprocess
import os
import threading
from subprocess import TimeoutExpired


def run_python(base_dir, timeout):
    out_file = open(os.path.join(base_dir, "out.txt"), 'wb')
    try:
        subprocess.run(["python3", os.path.join(base_dir, 'start.py')],
                           stdout=out_file, stderr=out_file, cwd=base_dir, timeout=timeout)
    # TODO добавить историю файлов (in_old)
    except TimeoutExpired as e:
        out_file.write(bytearray("Process has timed out after {} seconds".format(timeout), encoding='utf-8'))
    finally:
        out_file.close()


def run_exe(base_dir):
    pass


if __name__ == '__main__':
    test_path = "/Users/ilya/Documents/PycharmProjects/config/modules/Test"
    test2_path = "/Users/ilya/Documents/PycharmProjects/config/modules/Test_2"
    threading.Thread(target=run_python, args=(test_path, 0)).start()
    threading.Thread(target=run_python, args=(test2_path, 0)).start()
    # for i in range(500):
    #     threading.Thread(target=run_python, args=(test2_path,)).start()
    print("Done")
