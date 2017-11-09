import os
from time import sleep
import shutil

if __name__ == '__main__':
    # print(os.path.abspath(os.path.curdir))
    files = os.listdir('in')
    t = 0
    is_handle = False
    for file in files:
        if file != ".DS_Store":
            with open(os.path.join('in', file), 'r') as f:
                ln = f.read()
                t = int(ln.split(' ')[-1]) + 1
                print(ln)
                is_handle = True
    if is_handle:
        with open('out/finish.txt', 'w') as f:
            f.write("Данные из выхода первого модуля: {}".format(t))
        shutil.rmtree('in')
        os.mkdir('in')
