from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class Task(models.Model):
    summary = models.CharField(max_length=200, verbose_name='Краткое описание')
    description = models.TextField(blank=True, default='', verbose_name='Полное описание')
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус',
    )
    types = models.ManyToManyField(
        Type,
        related_name='tasks',
        verbose_name='Типы задачи',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')

    def __str__(self):
        return f'{self.pk}. {self.summary}'