from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Заголовок задачи")
    description = models.CharField(max_length=400, verbose_name="Описанеие задачи")
    # ответственный
    responsible = models.ForeignKey(User)
    # процесс выполнения
    finish_rate = models.IntegerField(default=0, verbose_name="Процесс выполнения")
    start_date = models.DateField(verbose_name="Дата начала задачи")
    deadline_date = models.DateField(verbose_name="Дата окончания задачи")

    def DateCorrectnessCheck(self):
        if self.start_date >= self.deadline_date:
            raise ValueError("Введены некорректные сроки начала и завершения задачи")

    def __str__(self):
        return self.name


class SubTask(models.Model):
    name = models.CharField(max_length=2000, verbose_name="Заголовок задачи")
    task = models.ForeignKey(Task, null=True)
    performer = models.ManyToManyField(User)
    is_finished = models.BooleanField(default=False)


    # role = models.CharField(max_length=100, verbose_name="Должность", default='Пользователь', blank=True)


# class Profile(models.Model):
#     ROLE_LIST = (('AD', 'Admin'), ('US', 'User'), ('LE', 'Leader'))
#     role = models.CharField(
#         max_length=2,
#         choices=ROLE_LIST,
#         default='US',
#     )
