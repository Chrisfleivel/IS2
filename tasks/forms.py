from django.forms import ModelForm
from .models import Task, EspacioDeTrabajo
from django import forms
from django.contrib.auth.models import User

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']



class EspacioDeTrabajoForm(forms.ModelForm):
    class Meta:
        model = EspacioDeTrabajo
        fields = ['nombre', 'miembros']
        widgets = {
            'miembros': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['miembros'].queryset = User.objects.filter(is_active=True)  # Filtrar solo usuarios activos


'''
class EspacioDeTrabajoForm2(ModelForm):
    class Meta:
        model = EspacioDeTrabajo
        fields = ['nombre', 'activo', 'miembros']
        widgets = {
            'miembros': forms.CheckboxSelectMultiple(),
        }

class TableroForm(ModelForm):
    class Meta:
        model = Tablero
        fields = ['nombre']

class ListaTareaForm(ModelForm):
    class Meta:
        model = ListaTarea
        fields = ['nombre']

class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre_actividad', 'descripcion', 'fecha_vencimiento', 'etiqueta']

        '''
