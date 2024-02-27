# Generated by Django 4.2.7 on 2024-02-27 01:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0021_alter_horario_atencion_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_agendada', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('horario_atencion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.horario_atencion')),
            ],
        ),
    ]
