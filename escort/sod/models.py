from django.db import models
from config.settings import BASE_DIR


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
    path = models.FilePathField(blank=True)
    description = models.TextField()
    periodic = models.IntegerField(default=60)
    timeout = models.IntegerField(default=10)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=STOPPED)
    sended_files = models.IntegerField(default=0)
    output_modules = models.ManyToManyField(to="self", blank=True)

    def make_module_directory(self, files):  # Возможно добавление логики замены модуля
        import os  # TODO Add slugify
        modules = os.path.join(BASE_DIR, "modules")
        module_dir = os.path.abspath(os.path.join(modules, self.name))
        os.mkdir(module_dir)
        os.mkdir(os.path.join(module_dir, 'in'))
        os.mkdir(os.path.join(module_dir, 'out'))
        print(files)
        for file in files:
            with open(os.path.join(module_dir, str(file)), 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        self.path = module_dir
        self.save()

    def __str__(self):
        return self.name
