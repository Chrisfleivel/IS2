# Generated by Django 5.1.1 on 2024-10-20 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_tarjeta_lista_alter_tarjeta_estado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarea',
            old_name='user',
            new_name='usuario_asignado',
        ),
    ]
