from django.contrib import admin
from .models import Task, EspacioDeTrabajo, Tablero, ListaTarea, Tarea
# Administra la pagina del administrador

class TaskAdmin(admin.ModelAdmin):
    # solo lectura
    readonly_fields = ("created", ) 
    


# Registro de los modelos que aparecen en la pagina del administrador
admin.site.register(Task, TaskAdmin)
admin.site.register(EspacioDeTrabajo)
admin.site.register(Tablero)
admin.site.register(ListaTarea)
admin.site.register(Tarea)
