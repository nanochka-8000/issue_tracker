from django import forms

from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['summary', 'description', 'types', 'status']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'types': forms.CheckboxSelectMultiple,
            'status': forms.Select(attrs={'class': 'form-select'}),
        }