from django.contrib import admin

from webapp.models import Project, Status, Task, Type


admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Task)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'started_at', 'finished_at')
    filter_horizontal = ('users',)