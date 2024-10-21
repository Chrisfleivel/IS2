from django.forms import ModelForm
from .models import Task, EspacioDeTrabajo, Tablero, Lista, Tarjeta, Tarea
from django import forms
from django.contrib.auth.models import User
from datetime import date


        
class FiltroTarjetasForm(forms.Form):
    usuario_asignado = forms.ModelChoiceField(queryset=None, required=False, label="Filtrar por Usuario:")

    def __init__(self, *args, **kwargs):
        usuarios = kwargs.pop('usuarios', None)
        super().__init__(*args, **kwargs)
        if usuarios:
            self.fields['usuario_asignado'].queryset = usuarios


class FiltroTarjetasEtiquetaForm(forms.Form):
    etiqueta = forms.CharField(max_length=50, required=False, label="Filtrar por Etiqueta:")



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


class TableroForm(ModelForm):
    class Meta:
        model = Tablero
        fields = ['nombre']



class ListaForm(ModelForm):
    class Meta:
        model = Lista
        fields = ['nombre', 'max_wip']


class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento', 'important', 'usuario_asignado', 'estado_cerrado']
        readonly_fields = ('fecha_creacion', 'atrasada') # solo lectura
        widgets = {
            'usuario_asignado': forms.Select(),
        } 

    def introducir_usuarios(self, usuarios):
        self.fields['usuario_asignado'].queryset =  usuarios
        

class TarjetaForm(ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['nombre_actividad', 'descripcion', 'fecha_vencimiento', 'usuario_asignado','etiqueta', 'estado']
        readonly_fields = ('fecha_creacion', 'tareas') # solo lectura
        widgets = {
            'usuario_asignado': forms.Select(),
            'estado': forms.Select(),
        } 

    def introducir_usuarios(self, usuarios):
        self.fields['usuario_asignado'].queryset =  usuarios
    
    def introducir_estados(self, estados):
        self.fields['estado'].queryset = estados

    def clean_fecha_vencimiento(self):
        # ... validación de fecha de vencimiento
        fecha_vencimiento = self.cleaned_data['fecha_vencimiento']
        if fecha_vencimiento < date.today():
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a hoy.")
        return fecha_vencimiento
