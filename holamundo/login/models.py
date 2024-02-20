from django.db import models
from django.utils import timezone

from django.urls import reverse




class Abogado(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Penal', 'Penal'),
        ('Laboral', 'Laboral'),
        ('Civil', 'Civil'),
    ]
    cedula = models.CharField(max_length=12, blank=False, null=True, default='')
    nombrea = models.CharField(max_length=144, blank=False, null=False)
    apellido = models.CharField(max_length=144, blank=False, null=False)
    celular = models.CharField(max_length=10, blank=False, null=False)
    correo = models.CharField(max_length=144, blank=False, null=False)
    tipos_especialidad = models.CharField(max_length=10, default='Penal', choices=ESPECIALIDAD_CHOICES)
    
    def __str__(self) -> str:
        return f'{self.nombrea}'

 
class Clientes(models.Model):
    # Atributos del cliente
    cedula = models.CharField(max_length=12, blank=False, null=True, default='')
    nombrec = models.CharField(max_length=144, blank=False, null=False)
    apellido = models.CharField(max_length=144, blank=False, null=False)
    direccion = models.CharField(max_length=144, blank=False, null=False)
    celular = models.CharField(max_length=10, blank=False, null=False)
    correo = models.CharField(max_length=144, blank=False, null=False)

    def __str__(self):
        return f'{self.nombrec}' 


class Cita(models.Model):
    abogado = models.ForeignKey(Abogado, related_name='citas', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, related_name='citas', on_delete=models.CASCADE)
    fecha_cita = models.DateTimeField()
    lugar_cita = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'Cita con {self.abogado.nombrea} el {self.fecha_cita}'

    
    def __str__(self) -> str:
        return f'{self.pk} - {self.cliente}'
    
    def get_absolute_url(self):
        return reverse('ver_cita', kwargs={'codigo_cita': self.pk})
    def get_edit_url(self):
        return reverse('editar_cita', kwargs={'codigo_cita': self.pk})
    
    def get_delete_url(self):
        return reverse('eliminar_cita', kwargs={'codigo_cita': self.pk})


class Casos(models.Model):
        CASOS_CHOICES=[
      ('Penal', 'Penal'),
      ('laboral', 'Laboral'),
      ('Civil','Civil'),
      ]
        ESTADO_CHOICES=[
      ('Proceso', 'Proceso'),
      ('Cerrado', 'Cerrado'),
      ]
    # Atributos de los casos
        abogado = models.ForeignKey(Abogado, related_name='casos', on_delete=models.CASCADE)
        cliente = models.ForeignKey(Clientes, related_name='casos', on_delete=models.CASCADE)
        tipos_casos = models.CharField(max_length=10, default='Penal', choices=CASOS_CHOICES)
        Estado = models.CharField(max_length=10, default='Proceso', choices=ESTADO_CHOICES)
        fecha_apertura = models.DateTimeField(default=timezone.now)
        descripcion = models.TextField(blank=True, null=True)

        def __str__(self) -> str:
            return f'El abogado {self.abogado.nombrea} trata al cliente {self.cliente.nombrec}'
        
class Documentos(models.Model):
    # Atributos del documento
    caso = models.ForeignKey(Casos, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion_documento = models.TextField()
    archivo_adjunto = models.FileField(upload_to='documentos/', blank=True, )

    def __str__(self) -> str:
        return f'Documento {self.tipo_documento} para el caso {self.caso.id}'
        
    def get_absolute_url(self):
        return reverse('ver_documento', kwargs={'codigo_documento': self.pk})
    
    def get_edit_url(self):
        return reverse('editar_documento', kwargs={'codigo_documento': self.pk})
    
    def get_delete_url(self):
        return reverse('eliminar_documento', kwargs={'codigo_documento': self.id})  
    
        