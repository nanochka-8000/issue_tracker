from django import template

register = template.Library()


@register.filter
def is_in_project(user, project):
    if not user.is_authenticated:
        return False
    return project.users.filter(pk=user.pk).exists()


@register.filter
def in_group(user, group_name):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()