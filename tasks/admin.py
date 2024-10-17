from django.contrib import admin
from .models import Task, EspacioDeTrabajo, Tablero, Lista, Tarea
# Administra la pagina del administrador

class TaskAdmin(admin.ModelAdmin):
    # solo lectura
    readonly_fields = ("created", ) 
    
class EspacioAdmin(admin.ModelAdmin):
    # solo lectura
    readonly_fields = ("creador", "activo", ) 

class TableroAdmin(admin.ModelAdmin):
    # solo lectura
    readonly_fields = ("espacio_trabajo", "listas", ) 

class ListaAdmin(admin.ModelAdmin):
    # solo lectura
    readonly_fields = ("tablero", "numero_tareas", "esta_llena", "posicion", "ultimo", ) 


# Registro de los modelos que aparecen en la pagina del administrador
admin.site.register(Task, TaskAdmin)
admin.site.register(EspacioDeTrabajo, EspacioAdmin)
admin.site.register(Tablero, TableroAdmin)
admin.site.register(Lista)
admin.site.register(Tarea)
