from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


# Create your models here.
'''
class Task(models.Model):
    title = models.CharField(max_length=100)   #texto
    description = models.TextField(blank=True)  # texto largo
    created = models.DateTimeField(auto_now_add=True)  #fecha creacion
    datecoplete = models.DateTimeField(null=True)  # fecha a terminar 
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
class Workspace(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    is_active = models.BooleanField(default=True)
'''