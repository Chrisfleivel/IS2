# Generated by Django 5.1.1 on 2024-10-19 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_tarea_atrasada_alter_tarjeta_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarjeta',
            name='lista',
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarjeta_estado', to='tasks.lista'),
        ),
    ]