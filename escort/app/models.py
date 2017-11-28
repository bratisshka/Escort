from django.db import models


# Create your models here.
class News(models.Model):
    header = models.CharField(max_length=300, verbose_name="Заголовок")
    content = models.CharField(max_length=300, blank=True, verbose_name="Содержимое", )
    image = models.FileField(upload_to='news/%Y/%m/%d/', blank=True, verbose_name="Изображение")
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    own = models.BooleanField(verbose_name="Аналитическая?", default=True)

    def __str__(self):
        return str(self.header)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Document(models.Model):
    description = models.TextField(verbose_name="Описание")
    file = models.FileField(upload_to='documents/')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
