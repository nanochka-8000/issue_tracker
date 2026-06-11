from django import forms

from webapp.models import Status, Type


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