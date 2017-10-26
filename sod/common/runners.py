import subprocess
import os
import threading


def run_python(base_dir):
    out_file = open(os.path.join(base_dir, "out.txt"), 'wb')
    t = subprocess.run(["python3", os.path.join(base_dir, 'start.py')],
                       stderr=out_file, cwd=base_dir)
    return t


if __name__ == '__main__':
    test_path = "/Users/ilya/Documents/PycharmProjects/Escort/modules/Test"
    test2_path = "/Users/ilya/Documents/PycharmProjects/Escort/modules/Test_2"
    threading.Thread(target=run_python, args=(test_path,)).start()
    threading.Thread(target=run_python, args=(test2_path,)).start()
    for i in range(500):
        threading.Thread(target=run_python, args=(test2_path,)).start()
    print("Done")