from django.http import HttpResponseForbidden
from .models import EspacioDeTrabajo

def obtener_espacio_trabajo(espacio_id):
    try:
        espacio = EspacioDeTrabajo.objects.get(id=espacio_id)
        return espacio
    except EspacioDeTrabajo.DoesNotExist:
        # Manejar la excepción si el espacio no existe
        return None
    

def miembro_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        espacio_trabajo = obtener_espacio_trabajo(kwargs['espacio_id'])  # Reemplaza con tu lógica para obtener el espacio
        if request.user in espacio_trabajo.miembros.all():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('No tienes permiso para acceder a este espacio.')
    return wrapper

