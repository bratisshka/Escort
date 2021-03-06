import os

from django.db import models
from pathlib import Path

from django.urls import reverse

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

    name = models.CharField(max_length=200, unique=True, verbose_name="Имя модуля")
    extension = models.CharField(max_length=10, choices=EXTENSION_CHOICES, verbose_name="Расширение")
    purpose = models.CharField(max_length=100, choices=File.PURPOSE_CHOICES, verbose_name="Тип входящих файлов")
    directory_name = models.CharField(blank=True, max_length=200)
    description = models.TextField(verbose_name="Описание")
    periodic = models.IntegerField(default=60, verbose_name="Периодичность")
    timeout = models.IntegerField(default=10, verbose_name="Таймаут")
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=STOPPED, verbose_name="Состояние")
    sended_files = models.IntegerField(default=0, verbose_name="Количество посланных файлов")
    output_modules = models.ManyToManyField(to="self",
                                            symmetrical=False,
                                            through='Dependancy',
                                            through_fields=('input_module', 'output_module'),
                                            blank=True,
                                            related_name='input_modules')
    is_service = models.BooleanField(default=False, verbose_name="Служебный?")
    last_executed = models.DateTimeField(auto_now_add=True, verbose_name="Последний запуск")

    class Meta:
        verbose_name = "модуль"
        verbose_name_plural = "модули"

    def get_absolute_url(self):
        return reverse('sod:module', args=(self.id,))

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

    #  Я не соблюдаю DRY для того, чтобы можно было их использовать в template
    @property
    def len_input(self):
        return len(os.listdir(str(self.get_module_directory() / 'in')))

    @property
    def len_output(self):
        return len(os.listdir(str(self.get_module_directory() / 'out')))

    @property
    def running(self):
        return self.state == self.RUNNING

    def append_to_input(self, files, to_in=True):
        if to_in:
            input_dir = str(self.get_module_directory() / 'in')
        else:
            input_dir = str(self.get_module_directory())
        for file in files:
            with open(os.path.join(input_dir, str(file)), 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

    def show_output_file(self):
        try:
            f = open(str(self.get_module_directory() / 'out.txt'), 'r')
            out = f.read()
        except FileNotFoundError:
            out = ""
        return out

    def show_log_file(self):
        try:
            f = open(str(self.get_module_directory() / 'log.txt'), 'r')
            log = f.read()
        except FileNotFoundError:
            log = ""
        return log


class Dependancy(models.Model):
    input_module = models.ForeignKey(Module, related_name='+')
    output_module = models.ForeignKey(Module, related_name='+')

    # class ServiceModule(models.Model):
    #     """
    #         Служебный модуль.
    #         Особенности:
    #          - создается и управляется только из своей админки
    #          - должен иметь доступ к своим настройкам, либо настраивается сам
    #          - не имеет родителей, только потоков
    #          - выполняется отдельно от остальных
    #         Примеры:
    #          - модуль, отвечающий за прослушивание и распределение входящих файлов
    #          - модуль, отвечающий за выкладывание результатов выполнения других модулей на портал
    #          - модуль, собирающий всю статистику, и генерирующий .pdf документ
    #
    #     """
    #     name = models.CharField(max_length=200, unique=True, verbose_name="Имя модуля")
    #     description = models.TextField(verbose_name="Описание")
