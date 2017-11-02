import os

from django.db import models
from pathlib import Path

from config.settings import MODULES_DIR


# Create your models here.
class File:
    TEXT, IMAGE, MUSIC, CRYPTO = 'text', 'image', 'music', 'crypto'
    PURPOSE_CHOICES = (
        (TEXT, 'Текст'),
        (IMAGE, 'Изображения'),
        (MUSIC, 'Музыка'),
        (CRYPTO, 'Крипта')
    )


class Module(models.Model):
    MAT, PY, EXE = 'm', 'py', 'exe'
    EXTENSION_CHOICES = (
        (MAT, 'Matlab'),
        (PY, 'Python'),
        (EXE, 'Execution')
    )
    RUNNING, STOPPED = 'run', 'stop'
    STATE_CHOICES = (
        (RUNNING, 'Running'),
        (STOPPED, 'Stopped')
    )
    SUPPORTED_EXTENSIONS = (MAT, PY, EXE)

    name = models.CharField(max_length=200, unique=True)
    extension = models.CharField(max_length=10, choices=EXTENSION_CHOICES)
    purpose = models.CharField(max_length=100, choices=File.PURPOSE_CHOICES)
    directory_name = models.CharField(blank=True, max_length=200)
    description = models.TextField()
    periodic = models.IntegerField(default=60)
    timeout = models.IntegerField(default=10)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=STOPPED)
    sended_files = models.IntegerField(default=0)
    output_modules = models.ManyToManyField(to="self", blank=True)

    def make_module_directory(self, files):  # Возможно добавление логики замены модуля
        """
        Создает директорию с модулем в файловой системе
        :param files: Файлы из запроса
        """

        module_dirname = self.make_directory_name()
        module_dir = str(MODULES_DIR / module_dirname)

        os.mkdir(module_dir)
        os.mkdir(os.path.join(module_dir, 'in'))
        os.mkdir(os.path.join(module_dir, 'out'))

        for file in files:
            with open(os.path.join(module_dir, str(file)), 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        self.directory_name = str(module_dirname)
        self.save()

    def get_module_directory(self):
        """
        :return: Path object
        """
        return MODULES_DIR / self.directory_name

    def make_directory_name(self):
        """
        Создает валидное в Windows имя папки, осуществляет проверку на уникальность
        """
        bad_symbols = set('!@#$%^&*":;<>,.?/|\\')
        bad_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                     'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        name = self.name
        for symbol in bad_symbols:
            if symbol in name:
                name.replace(symbol, "")
        if name in bad_names or os.path.exists(str(MODULES_DIR / name)):
            name = "Module {}".format(self.id)
        return name

    def __str__(self):
        return self.name
