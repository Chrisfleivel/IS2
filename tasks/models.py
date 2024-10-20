from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from ordered_model.models import OrderedModel

# Create your models here.



class EspacioDeTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='espacios_creados')
    miembros = models.ManyToManyField(User, related_name='espacios')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + ' - ' + self.creador.username
    
    def es_creador(self, user):
        return self.creador == user
    
    def miembros_a_elegir(self):
        return self.miembros


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
        print(lista1.orden)
        lista1.orden, lista2.orden = lista2.orden, lista1.orden
        print(lista1.orden)
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
    max_wip = models.IntegerField(validators=[MinValueValidator(1)])
    orden = models.PositiveIntegerField(default=0) 
    tarjetas = models.ManyToManyField('Tarjeta', related_name='lista_tarjetas') 
    lleno = models.BooleanField(default=False)

    class Meta:
        ordering = ['orden']

    def aumentar_n_tareas(self):
        self.numero_tareas = 1 + self.numero_tareas

    def agregar_tarjeta(self, tarjeta):
        '''Se agrega una tarjeta a tarjetas.
        Args:
            tarjetas (QuerySet): Un QuerySet de objetos.'''
        # Obtener el siguiente orden disponible
        self.tarjetas.add(tarjeta)
        self.numero_tareas = self.numero_tareas + 1
        if self.max_wip == self.numero_tareas:
            self.lleno = True
        self.save()

    def eliminar_tarjeta(self, tarjeta):
        """Elimina una o más listas y reordena las restantes.
        Args:
            listas (QuerySet): Un QuerySet de objetos Lista a eliminar.
        """
        # Eliminar la tarjeta seleccionada
        self.tarjetas.remove(tarjeta)
        # verificar si fue removida
        self.numero_tareas = self.numero_tareas - 1
        if self.max_wip > self.numero_tareas:
            self.lleno = False
        self.save()

    def __str__(self):
        return self.nombre + ' - ' + self.tablero.nombre
    
    def esta_lleno(self):
        '''Retorna True si el numero de tareas es igual al max wip'''
        return self.lleno
    

class Tarjeta(models.Model):
    nombre_actividad = models.CharField(max_length=255)
    estado = models.ForeignKey(Lista, on_delete=models.CASCADE, related_name='tarjeta_estado')
    usuario_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=1000)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    etiqueta = models.CharField(max_length=50, null=True, blank=True)
    tareas = models.ManyToManyField('Tarea', related_name='tareas_tarjeta') 

    def agregar_tarea(self, tarea):
        '''Se agrega una tarea a tareas.
        Args:
            tareas (QuerySet): Un QuerySet de objetos.'''
        # Obtener el siguiente orden disponible
        self.tareas.add(tarea)
        self.save()

    def eliminar_tarea(self, tarea):
        """Elimina una o más listas y reordena las restantes.
        Args:
            listas (QuerySet): Un QuerySet de objetos Lista a eliminar.
        """
        # Eliminar la tarjeta seleccionada
        self.tareas.remove(tarea)
        self.save()

    def __str__(self):
        return self.nombre_actividad 


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    usuario_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estado_cerrado = models.BooleanField(default=False)
    atrasada = models.BooleanField(default=False)
    

    def __str__(self):
        return self.titulo 


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    espacios = models.ManyToManyField('EspacioDeTrabajo', related_name='usuario_espacio')

    def actualizar(self):
        espacios = EspacioDeTrabajo.objects.filter(miembros=self.user)
        for espacio in espacios:
            self.espacios.add(espacio)
    
    def agregar_espacio(self, espacio):
        self.espacios.add(espacio)

    def quitar_espacio(self, espacio):
        self.espacios.remove(espacio)

    def __str__(self):
        return self.user.username

