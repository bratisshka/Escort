import os
from time import sleep
import shutil

if __name__ == '__main__':
    # print(os.path.abspath(os.path.curdir))
    files = os.listdir('in')
    t = 0
    is_handle = False
    for file in files:
        with open(os.path.join('in', file), 'r') as f:
            ln = f.read()
            t = int(ln.split(' ')[-1]) + 1
            print(ln)
            is_handle = True

    if is_handle:
        print("top kek")
        with open('out/finish.txt', 'w') as f:
            f.write("Данные из выхода второго модуля: {}".format(t))
        shutil.rmtree(os.path.abspath('in'))
        os.mkdir('in')
