from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ProjectForm, ProjectUsersForm, TaskForm
from webapp.models import Project, Task



class TaskListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all().order_by('-created_at')
        return context


class TaskDetailView(TemplateView):
    template_name = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['task'] = get_object_or_404(Task, pk=pk)
        return context


class TaskCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_create.html', {'form': form})

    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = Task.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                project=form.cleaned_data['project'],
            )
            task.types.set(form.cleaned_data['types'])
            return redirect('task_list')
        return render(request, 'task_create.html', {'form': form})


class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(initial={
            'summary': task.summary,
            'description': task.description,
            'types': task.types.all(),
            'status': task.status,
            'project': task.project,
        })
        return render(request, 'task_update.html', {'form': form, 'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.summary = form.cleaned_data['summary']
            task.description = form.cleaned_data['description']
            task.status = form.cleaned_data['status']
            task.project = form.cleaned_data['project']
            task.save()
            task.types.set(form.cleaned_data['types'])
            return redirect('task_detail', pk=task.pk)
        return render(request, 'task_update.html', {'form': form, 'task': task})


class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'task_delete.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('task_list')



class ProjectListView(TemplateView):
    template_name = 'project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context


class ProjectDetailView(TemplateView):
    template_name = 'project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['project'] = get_object_or_404(Project, pk=pk)
        return context


class ProjectCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProjectForm()
        return render(request, 'project_create.html', {'form': form})

    def post(self, request):
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            project = form.save()
            project.users.add(request.user)
            return redirect('project_detail', pk=project.pk)
        return render(request, 'project_create.html', {'form': form})


class ProjectUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(instance=project)
        return render(request, 'project_update.html', {'form': form, 'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
        return render(request, 'project_update.html', {'form': form, 'project': project})


class ProjectDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'project_delete.html', {'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect('project_list')


class ProjectAddUsersView(LoginRequiredMixin, View):

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectUsersForm(instance=project)
        return render(request, 'project_add_users.html', {'form': form, 'project': project})

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectUsersForm(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
        return render(request, 'project_add_users.html', {'form': form, 'project': project})


class ProjectRemoveUserView(LoginRequiredMixin, View):

    def post(self, request, pk, user_pk):
        project = get_object_or_404(Project, pk=pk)
        user = get_object_or_404(User, pk=user_pk)
        project.users.remove(user)
        return redirect('project_detail', pk=project.pk)