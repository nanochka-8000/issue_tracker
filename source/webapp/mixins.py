from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from webapp.models import Project, Task


from django.shortcuts import render


class PermissionDeniedMixin(UserPassesTestMixin):

    permission_denied_message = 'У вас недостаточно прав для этого действия.'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return render(self.request, '403.html', {'exception': self.permission_denied_message}, status=403)



class CanCreateProjectMixin(PermissionDeniedMixin):

    def test_func(self):
        return self.request.user.has_perm('webapp.add_project')


class CanEditProjectMixin(PermissionDeniedMixin):

    def test_func(self):
        user = self.request.user
        if not user.has_perm('webapp.change_project'):
            return False
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return project.users.filter(pk=user.pk).exists()


class CanManageUsersMixin(PermissionDeniedMixin):

    def test_func(self):
        user = self.request.user
        # Менеджер или Капитан
        allowed_groups = {'Project Manager', 'Team Lead'}
        user_groups = set(user.groups.values_list('name', flat=True))
        if not (allowed_groups & user_groups):
            return False
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return project.users.filter(pk=user.pk).exists()




class CanCreateTaskMixin(PermissionDeniedMixin):

    def test_func(self):
        user = self.request.user
        if not user.has_perm('webapp.add_task'):
            return False
        return user.projects.exists()


class CanEditTaskMixin(PermissionDeniedMixin):

    def test_func(self):
        user = self.request.user
        if not user.has_perm('webapp.change_task'):
            return False
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if task.project is None:
            return user.is_superuser
        return task.project.users.filter(pk=user.pk).exists()


class CanDeleteTaskMixin(PermissionDeniedMixin):

    def test_func(self):
        user = self.request.user
        if not user.has_perm('webapp.delete_task'):
            return False
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if task.project is None:
            return user.is_superuser
        return task.project.users.filter(pk=user.pk).exists()