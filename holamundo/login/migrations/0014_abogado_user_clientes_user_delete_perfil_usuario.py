# Generated by Django 4.2.7 on 2024-02-22 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0013_merge_20240221_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='abogado',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='perfila', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientes',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Perfil_Usuario',
        ),
    ]
