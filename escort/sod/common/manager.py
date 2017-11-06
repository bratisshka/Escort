import os
import threading
import shutil

import django  # For testing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from escort.sod.common.settings import MODULES_DIR, PATH_FOR_MUSIC, PATH_FOR_IMAGES, PATH_FOR_TXT
from escort.sod.models import Module, File
from escort.sod.common.runners import run_python, run_exe
from escort.sod.common.settings import TIME_TO_SEND_FILES

PURPOSE_MAP = {
    File.TEXT: PATH_FOR_TXT,
    File.MUSIC: PATH_FOR_MUSIC,
    File.IMAGE: PATH_FOR_IMAGES,
    File.CRYPTO: PATH_FOR_TXT
}


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def clean_directory(path_to_module):
    try:
        shutil.rmtree(path_to_module)
        os.mkdir(path_to_module)
    except OSError:
        print("Неправильная директория {}".format(path_to_module))


class ModuleManager:
    @staticmethod
    def run_module(module_id):
        mod = Module.objects.get(pk=module_id)
        if mod.extension == 'py':
            runner = run_python
        elif mod.extension == 'exe':
            runner = run_exe
        else:
            raise FileNotFoundError("Unsupported Extension")
        thread = threading.Thread(target=runner, args=(str(mod.get_module_directory()), mod.timeout))
        thread.start()
        return thread

    @staticmethod
    def clean_input_data(module_id):
        mod = Module.objects.get(pk=module_id)
        clean_directory(str(mod.get_module_directory() / 'in'))

    @staticmethod
    def clean_output_data(module_id):
        mod = Module.objects.get(pk=module_id)
        clean_directory(str(mod.get_module_directory() / 'out'))

    @staticmethod
    def make_out_archive(module_id):
        mod = Module.objects.get(pk=module_id)
        filename = mod.name + '.zip'
        shutil.make_archive(str(MODULES_DIR / mod.name / mod.name), 'zip', str(mod.get_module_directory() / 'out'))
        return str(MODULES_DIR / mod.name / filename), filename

    @staticmethod
    def send_default_files(modules):
        """ Посылает файлы из входящей папки согласно типу обрабатываемых"""
        for module in modules:
            try:
                input_dir = PURPOSE_MAP[module.purpose]
                copytree(input_dir, str(module.get_module_directory() / 'in'))
            except KeyError:
                print("Значение {} не поддерживается".format(module.purpose))
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
                    copytree(str(module.get_module_directory() / 'out'), str(out_module.get_module_directory() / 'in'))
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
