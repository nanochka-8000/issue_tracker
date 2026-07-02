from django import forms

from webapp.models import Project, Status, Type


class TaskForm(forms.Form):
    summary = forms.CharField(
        max_length=200,
        label='Краткое описание',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    description = forms.CharField(
        required=False,
        label='Полное описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
    )
    types = forms.ModelMultipleChoiceField(
        queryset=Type.objects.all(),
        label='Типы',
        widget=forms.CheckboxSelectMultiple,
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label='Проект',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'started_at', 'finished_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'started_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finished_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'started_at': 'Дата начала',
            'finished_at': 'Дата окончания',
        }


class ProjectUsersForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['users']
        widgets = {
            'users': forms.CheckboxSelectMultiple,
        }
        labels = {'users': 'Участники'}