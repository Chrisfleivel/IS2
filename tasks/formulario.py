from django import forms
from django.forms import ModelForm
from .models import EspacioDeTrabajo, User, Task

class EspacioForm(forms.ModelForm):
    miembros = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    class Meta:
        model = EspacioDeTrabajo
        fields = ['nombre', 'miembros']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

