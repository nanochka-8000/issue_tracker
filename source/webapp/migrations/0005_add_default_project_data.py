from datetime import date

from django.db import migrations


def create_default_project(apps, schema_editor):
    Project = apps.get_model('webapp', 'Project')
    Task = apps.get_model('webapp', 'Task')

    project, _ = Project.objects.get_or_create(
        name='Тестовый проект',
        defaults={
            'description': 'Создан автоматически при миграции для существующих задач.',
            'start_date': date.today(),
        },
    )
    Task.objects.filter(project__isnull=True).update(project=project)


def remove_default_project(apps, schema_editor):
    Task = apps.get_model('webapp', 'Task')
    Task.objects.update(project=None)


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_project_task_project'),
    ]

    operations = [
        migrations.RunPython(create_default_project, remove_default_project),
    ]