# Generated by Django 4.2.7 on 2024-02-27 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0022_cita1'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita1',
            name='hora_elegida',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]