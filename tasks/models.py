from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


from django.db.models.signals import post_save
from django.dispatch import receiver

from ordered_model.models import OrderedModel

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username


class EspacioDeTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='espacios_creados')
    miembros = models.ManyToManyField(User, related_name='espacios')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + ' - ' + self.creador.username
    
    def es_creador(self, user):
        return self.creador == user


class Tablero(models.Model):
    nombre = models.CharField(max_length=100)
    espacio_trabajo = models.ForeignKey(EspacioDeTrabajo, on_delete=models.CASCADE, related_name='tableros')
    listas = models.ManyToManyField('Lista', related_name='tablas')

    def agregar_lista(self, lista):
        '''Se agrega una lista a listas y se ordena al final.
        Args:
            listas (QuerySet): Un QuerySet de objetos.'''
        # Obtener el siguiente orden disponible
        last_lista = self.listas.last()
        if last_lista:
            new_order = last_lista.orden + 1
        else:
            new_order = 0
        lista.orden = new_order
        lista.save()
        self.listas.add(lista)
        self.save()

    def cambiar_orden(self, lista1, lista2):
        """Cambia el orden de las listas recibidas con respecto a self.listas"""
        if lista1 not in self.listas.all() or lista2 not in self.listas.all():
            raise ValueError("Las listas no pertenecen a este tablero")

        lista1.orden, lista2.orden = lista2.orden, lista1.orden
        lista1.save()
        lista2.save()

    def eliminar_lista(self, lista_recibida):
        """Elimina una o más listas y reordena las restantes.
        Args:
            listas (QuerySet): Un QuerySet de objetos Lista a eliminar.
        """
        # Eliminar la lista seleccionada
        self.listas.remove(lista_recibida)
        # Reordenar las listas restantes
        order = 0
        for lista in self.listas.all():
            lista.orden = order
            lista.save()
            order += 1

    def __str__(self):
        return self.nombre + ' - ' + self.espacio_trabajo.nombre
    

class Lista(OrderedModel, models.Model):
    nombre = models.CharField(max_length=100)
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='listas_t')
    numero_tareas = models.IntegerField(default=0)
    max_wip = models.IntegerField() 
    orden = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['orden']

    def aumentar_n_tareas(self):
        self.numero_tareas = 1 + self.numero_tareas
    
    def disminuir_n_tareas(self):
        self.numero_tareas = self.numero_tareas - 1

    def __str__(self):
        return self.nombre + ' - ' + self.tablero.nombre
    
    def is_over_wip(self):
        return self.tareas.count() > self.max_wip
    
    def esta_lleno(self):
        '''Retorna True si el numero de tareas es igual al max wip'''
        return self.numero_tareas == self.max_wip

    def mover_a_la_derecha(self):
        return self.orden > 0

    def mover_a_la_izquierda(self):
        return self.ultimo

          
    def es_ultimo(self):
        return self.ultimo
    
    def posicionar_ultimo(self):
        self.ultimo = True

    def desposicionar_ultimo(self):
        self.ultimo = False
    

class Tarea(models.Model):
    nombre_actividad = models.CharField(max_length=255)
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='tareas')
    usuario_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completado', 'Completado')])
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    etiqueta = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nombre_actividad + ' - ' + self.lista.nombre
    

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

