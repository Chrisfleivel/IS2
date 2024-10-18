from django.forms import ModelForm
from .models import Task, EspacioDeTrabajo, Tablero, Lista, Tarjeta
from django import forms
from django.contrib.auth.models import User
from datetime import date


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
'''

class TareaForm(ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'vencimiento', 'important']

        
    creacion = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # estado = (abierto/cerrado)

'''
class TarjetaForm(ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['nombre_actividad', 'descripcion', 'fecha_vencimiento', 'usuario_asignado','etiqueta', 'estado']
        readonly_fields = ('lista','fecha_creacion', 'tarjeats') # solo lectura
        widgets = {
            'usuario_asignado': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario_asignado'].queryset =  User.objects.filter(is_active=True)  # Filtrar solo usuarios activos  

    def clean_fecha_vencimiento(self):
        # ... validación de fecha de vencimiento
        fecha_vencimiento = self.cleaned_data['fecha_vencimiento']
        if fecha_vencimiento < date.today():
            raise forms.ValidationError("La fecha de vencimiento no puede ser anterior a hoy.")
        return fecha_vencimiento
'''

        widgets = {
            'estado': Select(choices=ESTADO_CHOICES),
            'usuario_asignado': ModelChoiceField(queryset=Usuario.objects.all()),
        }'''


