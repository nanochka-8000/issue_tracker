from django.contrib import admin
from webapp.models import Status, Type, Task


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'status', 'created_at']
    list_filter = ['status', 'types']
    search_fields = ['summary', 'description']
    filter_horizontal = ['types']


admin.site.register(Status, StatusAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Task, TaskAdmin)