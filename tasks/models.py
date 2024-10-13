from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


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

    def __str__(self):
        return self.nombre + ' - ' + self.espacio_trabajo.nombre


class ListaTarea(models.Model):
    nombre = models.CharField(max_length=100)
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE, related_name='listas')
    numero_tareas = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre + ' - ' + self.tablero.nombre


class Tarea(models.Model):
    nombre_actividad = models.CharField(max_length=255)
    lista = models.ForeignKey(ListaTarea, on_delete=models.CASCADE, related_name='tareas')
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


'''
class CustomUser(AbstractUser):

    slug = models.SlugField(unique=True, blank=True)
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

'''