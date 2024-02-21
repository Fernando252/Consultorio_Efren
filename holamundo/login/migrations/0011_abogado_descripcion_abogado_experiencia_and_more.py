# Generated by Django 5.0.2 on 2024-02-21 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_merge_20240220_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='abogado',
            name='descripcion',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AddField(
            model_name='abogado',
            name='experiencia',
            field=models.CharField(default='', max_length=144),
        ),
        migrations.AddField(
            model_name='abogado',
            name='facebook',
            field=models.CharField(default='', max_length=144),
        ),
        migrations.AddField(
            model_name='abogado',
            name='instagram',
            field=models.CharField(default='', max_length=144),
        ),
        migrations.AddField(
            model_name='abogado',
            name='twitter',
            field=models.CharField(default='', max_length=144),
        ),
        migrations.AlterField(
            model_name='abogado',
            name='apellido',
            field=models.CharField(default='', max_length=144),
        ),
        migrations.AlterField(
            model_name='abogado',
            name='celular',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='abogado',
            name='correo',
            field=models.CharField(default='', max_length=144),
        ),
        migrations.AlterField(
            model_name='abogado',
            name='nombrea',
            field=models.CharField(default='', max_length=144),
        ),
    ]
