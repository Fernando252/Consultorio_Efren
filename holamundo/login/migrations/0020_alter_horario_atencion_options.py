# Generated by Django 4.2.7 on 2024-02-27 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_horario_atencion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='horario_atencion',
            options={'ordering': ['fecha']},
        ),
    ]
