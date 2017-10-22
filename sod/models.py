from django.db import models


# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=200)
    TEXT = 'text'
    IMAGE = 'image'
    MUSIC = 'music'
    CRYPTO = 'crypto'
    PURPOSE_CHOICES = (
        (TEXT, 'Текст'),
        (IMAGE, 'Изображения'),
        (MUSIC, 'Музыка'),
        (CRYPTO, 'Крипта')
    )
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES)
    file = models.FileField(upload_to='sod/files/')  # TODO возможно надо сделать функцию зависимость от purpose


class Module(models.Model):
    name = models.CharField(max_length=200)
    MAT = 'm'
    PY = 'py'
    EXE = 'exe'
    EXTENSION_CHOICES = (
        (MAT, 'Matlab'),
        (PY, 'Python'),
        (EXE, 'Execution')
    )
    extension = models.CharField(max_length=10, choices=EXTENSION_CHOICES)
    purpose = models.CharField(max_length=100, choices=File.PURPOSE_CHOICES)
    file = models.FileField(upload_to='sod/modules/')
    description = models.TextField()
