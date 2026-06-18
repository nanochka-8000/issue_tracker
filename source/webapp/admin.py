from django.contrib import admin
from webapp.models import Status, Type, Task, Project


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_date', 'end_date']
    search_fields = ['name', 'description']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'project', 'status', 'created_at']
    list_filter = ['status', 'types', 'project']
    search_fields = ['summary', 'description']
    filter_horizontal = ['types']


admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)