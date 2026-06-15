
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')
django.setup()

from datetime import timedelta
from django.db.models import Q, F, Count
from django.utils import timezone

from webapp.models import Task, Type


def header(title):
    print('\n' + '=' * 70)
    print(title)
    print('=' * 70)



header('1. Закрытые задачи за последний месяц')
one_month_ago = timezone.now() - timedelta(days=30)
closed_recent = Task.objects.filter(
    status__name='Done',
    updated_at__gte=one_month_ago,
)
for task in closed_recent:
    print(f'  #{task.pk} {task.summary} (обновлено {task.updated_at:%d.%m.%Y})')


header('2. (New | In Progress) И (Bug | Enhancement)')
filtered = Task.objects.filter(
    status__name__in=['New', 'In Progress'],
    types__name__in=['Bug', 'Enhancement'],
).distinct()
for task in filtered:
    types = ', '.join(t.name for t in task.types.all())
    print(f'  #{task.pk} {task.summary} [статус: {task.status.name}, типы: {types}]')


header('3. Не закрытые: summary~"bug" ИЛИ тип Bug')
not_done_bugs = Task.objects.filter(
    ~Q(status__name='Done')
).filter(
    Q(summary__icontains='bug') | Q(types__name='Bug')
).distinct()
for task in not_done_bugs:
    print(f'  #{task.pk} {task.summary} [статус: {task.status.name}]')


header('Бонус 1. Только нужные поля для всех задач')
rows = Task.objects.values('id', 'summary', 'types__name', 'status__name')
for row in rows:
    print(
        f'  #{row["id"]} {row["summary"]} | '
        f'тип: {row["types__name"]} | статус: {row["status__name"]}'
    )


header('Бонус 2. Задачи где summary == description')
same = Task.objects.filter(summary=F('description'))
for task in same:
    print(f'  #{task.pk} {task.summary}')


header('Бонус 3. Количество задач по каждому типу')
type_counts = Type.objects.annotate(task_count=Count('tasks')).order_by('-task_count')
for type_obj in type_counts:
    print(f'  {type_obj.name}: {type_obj.task_count}')