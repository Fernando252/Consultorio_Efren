# Generated by Django 5.0.2 on 2024-02-21 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_abogado_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abogado',
            name='foto',
            field=models.ImageField(blank=True, help_text='foto.', null=True, upload_to='foto_abogados/', verbose_name='foto'),
        ),
    ]
