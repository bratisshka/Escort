import django  # For testing

django.setup()

import os
import threading
import shutil
from sod.common.settings import MODULES_DIR, PATH_FOR_MUSIC, PATH_FOR_IMAGES, PATH_FOR_TXT
from sod.models import Module, File
from sod.common.runners import run_python, run_exe
from sod.common.settings import TIME_TO_SEND_FILES

PURPOSE_MAP = {
    File.TEXT: PATH_FOR_TXT,
    File.MUSIC: PATH_FOR_MUSIC,
    File.IMAGE: PATH_FOR_IMAGES,
    File.CRYPTO: PATH_FOR_TXT
}


def get_module_map(modules_path):
    return {file: os.path.abspath(os.path.join(modules_path, file)) for file in os.listdir(modules_path)}


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def clean_directory(path_to_module):
    shutil.rmtree(path_to_module)
    os.mkdir(path_to_module)


class ModuleManager:
    @staticmethod
    def run_module(module_id):
        mod = Module.objects.get(pk=module_id)
        if mod.extension == 'py':
            runner = run_python
        elif mod.extension == 'exe':
            runner = run_exe
        else:
            runner = lambda x: x  # Ну или исключение вызвать
        thread = threading.Thread(target=runner, args=(mod.path, mod.timeout))
        thread.start()
        return thread

    @staticmethod
    def clean_input_data(module_id):
        mod = Module.objects.get(pk=module_id)
        clean_directory(os.path.join(mod.path, 'in'))

    @staticmethod
    def clean_output_data(module_id):
        mod = Module.objects.get(pk=module_id)
        clean_directory(os.path.join(mod.path, 'out'))

    @staticmethod
    def send_default_files(modules):
        """ Посылает файлы из входящей папки согласно типу обрабатываемых"""
        for module in modules:
            input_dir = PURPOSE_MAP[module.purpose]
            copytree(input_dir, os.path.join(module.path, 'in'))
        for value in PURPOSE_MAP.values():
            clean_directory(value)

    @staticmethod
    def send_files_to_modules():
        """ Посылает файлы согласно графу выводов модулей """
        modules = Module.objects.all()
        for module in modules:
            if module.id == 1:  # Default Module
                ModuleManager.send_default_files(module.output_modules.all())
            else:
                for out_module in module.output_modules.all():
                    copytree(os.path.join(module.path, 'out/'), os.path.join(out_module.path, 'in/'))
                ModuleManager.clean_output_data(module.id)

    @staticmethod
    def start():
        """
        Основной цикл работы
        Для каждого вида действий (пересылка выводных файлов, запуск модулей) стоит свой таймер
        """
        from time import time
        started = time()
        seconds = 0
        while True:
            t = int(time() - started)
            if t == seconds:
                # Пересылка файлов
                if t % TIME_TO_SEND_FILES == 0:
                    print("Sending files: {}".format(t))
                    ModuleManager.send_files_to_modules()
                    # запуск модулей
                for module in Module.objects.all():
                    if module.state == Module.RUNNING:
                        if t % module.periodic == 0:
                            # print("Started module {}".format(module.name))
                            ModuleManager.run_module(module.id)
                seconds = int(time() - started) + 1
                # print(seconds)


if __name__ == '__main__':
    # ModuleManager.clean_input_data(7)
    # ModuleManager.run_module(7)
    # ModuleManager.send_files_to_modules()
    ModuleManager.start()
