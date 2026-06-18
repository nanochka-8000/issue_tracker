from django.db import models

from webapp.validators import validate_summary_capital, validate_no_placeholder


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')

    def __str__(self):
        return self.name


class Task(models.Model):
    summary = models.CharField(
        max_length=200,
        validators=[validate_summary_capital],
        verbose_name='Краткое описание',
    )
    description = models.TextField(
        blank=True,
        default='',
        validators=[validate_no_placeholder],
        verbose_name='Полное описание',
    )
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
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    def __str__(self):
        return f'{self.pk}. {self.summary}'