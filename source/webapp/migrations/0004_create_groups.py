from django.db import migrations


GROUPS_PERMISSIONS = {
    'Project Manager': [
        # Проекты
        ('add_project', 'webapp', 'project'),
        ('change_project', 'webapp', 'project'),
        ('delete_project', 'webapp', 'project'),
        ('view_project', 'webapp', 'project'),
        # Задачи
        ('add_task', 'webapp', 'task'),
        ('change_task', 'webapp', 'task'),
        ('delete_task', 'webapp', 'task'),
        ('view_task', 'webapp', 'task'),
    ],
    'Team Lead': [
        ('view_project', 'webapp', 'project'),
        ('add_task', 'webapp', 'task'),
        ('change_task', 'webapp', 'task'),
        ('delete_task', 'webapp', 'task'),
        ('view_task', 'webapp', 'task'),
    ],
    'Developer': [
        ('view_project', 'webapp', 'project'),
        ('add_task', 'webapp', 'task'),
        ('change_task', 'webapp', 'task'),
        ('view_task', 'webapp', 'task'),
    ],
}


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    for group_name, permissions in GROUPS_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        for codename, app_label, model in permissions:
            ct = ContentType.objects.get(app_label=app_label, model=model)
            perm = Permission.objects.get(content_type=ct, codename=codename)
            group.permissions.add(perm)


def delete_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=GROUPS_PERMISSIONS.keys()).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_project_task_project'),
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]