import datetime
import os
import threading
import shutil
from collections import defaultdict
from time import sleep

import django  # For testing
from multiprocessing import Process

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
FILE_EXTENSIONS = {
    'jpg': 'image',
    'png': 'image',
    'bmp': 'image',
    'wav': 'music',
    'mp3': 'music',
    'txt': 'text',
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
        # thread = threading.Thread(target=runner, args=(str(mod.get_module_directory()), mod.timeout))
        # thread.start()
        p = Process(target=runner, args=(str(mod.get_module_directory()), mod.timeout))
        p.start()
        return p

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
    def send_default_files():
        """ Посылает файлы из входящей папки согласно типу обрабатываемых"""
        module = Module.objects.get(pk=1)
        module_dir = module.get_module_directory()
        output_modules = module.output_modules.all()
        file_list = [file for file in os.listdir(str(module_dir)) if os.path.isfile(str(module_dir / file))]
        if len(file_list) > 0:  # будем что-то делать, если в папке что-то есть
            module_map = defaultdict(list)
            for purpose, module in ((module.purpose, module) for module in output_modules):
                module_map[purpose].append(module)
            for file_obj in file_list:
                file_extesion = file_obj.split('.')[-1]
                file_purpose = FILE_EXTENSIONS.get(file_extesion, -1)
                if file_purpose == -1:
                    print("{} не опознан".format(file_obj))
                    continue
                else:
                    modules_for_file = module_map[file_purpose]
                    if len(modules_for_file) == 0:
                        print("Отстуствуют подохдящие модули для {}".format(file_obj))
                        continue
                    for mod in modules_for_file:
                        shutil.copy2(str(module_dir / file_obj), str(mod.get_module_directory() / 'in' / file_obj))
                        mod.sended_files += 1
                        mod.save()
                os.remove(str(module_dir / file_obj))

    @staticmethod
    def send_files_to_modules():
        """ Посылает файлы согласно графу выводов модулей """
        modules = Module.objects.all()
        for module in modules:
            if module.id != 1:
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
        last_sended = datetime.datetime.now()
        while True:
            t = datetime.datetime.now()
            # Пересылка файлов
            if (t - last_sended).seconds > TIME_TO_SEND_FILES:
                print("Sending files at {}".format(t.strftime('%H:%M %d.%m.%Y')))
                ModuleManager.send_files_to_modules()
                last_sended = t
            # запуск модулей
            for module in Module.objects.all():
                if module.state == Module.RUNNING:
                    execute_time = datetime.datetime.now(datetime.timezone.utc)
                    if (execute_time - module.last_executed).seconds > module.periodic:
                        print("Started module {} at {}".format(module.name, execute_time.strftime("%H:%M %d.%m.%Y")))
                    if module.id == 1:  # Входящий поток
                        ModuleManager.send_default_files()
                    else:
                        ModuleManager.run_module(module.id)
                    module.last_executed = execute_time
                    module.save()
            sleep(30)


if __name__ == '__main__':
    # ModuleManager.clean_input_data(7)
    # ModuleManager.run_module(7)
    # ModuleManager.send_files_to_modules()
    if len(Module.objects.all()) == 0:
        m = Module(name="Входящий поток",
                   extension=Module.PY,
                   purpose=File.TEXT,
                   directory_name="Входящий поток",
                   description="Модуль по умолчанию. Слушает источники данных и перенаправляет их в подключенные модули",
                   periodic=1,
                   timeout=10,
                   state=Module.RUNNING,
                   )
        m.save()
    # ModuleManager.send_files_to_modules()
    ModuleManager.start()
    # ModuleManager.send_default_files(Module.objects.get(pk=1))
