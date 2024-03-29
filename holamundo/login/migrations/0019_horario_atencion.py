# Generated by Django 4.2.7 on 2024-02-27 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_casos_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario_atencion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.CharField(choices=[('08:00 a 09:00', '08:00 a 09:00'), ('09:00 a 10:00', '09:00 a 10:00'), ('10:00 a 11:00', '10:00 a 11:00'), ('11:00 a 12:00', '11:00 a 12:00'), ('14:00 a 15:00', '14:00 a 15:00'), ('15:00 a 16:00', '15:00 a 16:00'), ('16:00 a 17:00', '16:00 a 17:00')], max_length=50)),
                ('abogado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios_atencion', to='login.abogado')),
            ],
        ),
    ]
