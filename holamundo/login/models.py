from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Clientes(models.Model):
    # Atributos del cliente
    user = models.OneToOneField(User, related_name='cliente', on_delete=models.CASCADE,default=None)
    cedula = models.CharField(max_length=12, blank=False, null=True, default='')
    nombrec = models.CharField(max_length=144, blank=False, null=False)
    apellido = models.CharField(max_length=144, blank=False, null=False)
    direccion = models.CharField(max_length=144, blank=False, null=False)
    celular = models.CharField(max_length=10, blank=False, null=False)
    correo = models.CharField(max_length=144, blank=False, null=False)

    def __str__(self):
        return f'{self.nombrec}' 
    
class Abogado(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Penal', 'Penal'),
        ('Laboral', 'Laboral'),
        ('Civil', 'Civil'),  
    ]
    user = models.OneToOneField(User, related_name='abogado', on_delete=models.CASCADE,default=None)
    cedula = models.CharField(max_length=12, blank=False, null=True, default='')
    nombrea = models.CharField(max_length=144, blank=False, null=False,default='')
    apellido = models.CharField(max_length=144, blank=False, null=False,default='')
    celular = models.CharField(max_length=10, blank=False, null=False,default='')
    correo = models.CharField(max_length=144, blank=False, null=False,default='')
    experiencia = models.CharField(max_length=144, blank=False, null=False,default='')
    facebook = models.CharField(max_length=144, blank=False, null=False,default='')
    instagram = models.CharField(max_length=144, blank=False, null=False,default='')
    twitter = models.CharField(max_length=144, blank=False, null=False,default='')
    descripcion = models.TextField(blank=False, null=False, default='')
    tipos_especialidad = models.CharField(max_length=10, default='Penal', choices=ESPECIALIDAD_CHOICES)

    foto = models.ImageField(
        upload_to="foto_abogados/", 
        blank=True, 
        null=True, 
        verbose_name='foto',
        help_text='foto.',
    )
    
    def __str__(self) -> str:
        return f'{self.nombrea}'
    
    def get_absolute_url(self):
        return reverse('editar_abogado', kwargs={'codigo_abogado': self.pk})
 

class Horario_atencion(models.Model):
    HORAS_CHOICES = [
        ("08:00 a 09:00", "08:00 a 09:00"),
        ("09:00 a 10:00", "09:00 a 10:00"),
        ("10:00 a 11:00", "10:00 a 11:00"),
        ("11:00 a 12:00", "11:00 a 12:00"),
        ("14:00 a 15:00", "14:00 a 15:00"),
        ("15:00 a 16:00", "15:00 a 16:00"),
        ("16:00 a 17:00", "16:00 a 17:00"),
    ]

    abogado = models.ForeignKey(Abogado, related_name='horarios_atencion', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.CharField(max_length=50, choices=HORAS_CHOICES)


    def __str__(self):
        return f'{self.abogado.nombrea} - {self.fecha} - {self.hora}'
    def get_absolute_url(self):
        return reverse('registrar_cita', kwargs={'abogado_id': self.abogado.id, 'horario_id': self.id})
    
class Cita1(models.Model):
    cliente = models.ForeignKey(Clientes,related_name='cita1', on_delete=models.CASCADE)
    abogado = models.ForeignKey(Abogado, related_name='cita1',on_delete=models.CASCADE)
    horario_atencion = models.ForeignKey(Horario_atencion, on_delete=models.CASCADE)
    fecha_agendada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cita para {self.cliente.user} - {self.horario_atencion.fecha} - {self.horario_atencion.hora}'



    

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
    CASOS_CHOICES = [
        ('Penal', 'Penal'),
        ('Laboral', 'Laboral'),
        ('Civil', 'Civil'),
    ]
    ESTADO_CHOICES = [
        ('Proceso', 'Proceso'),
        ('Cerrado', 'Cerrado'),
    ]

    # Atributos de los casos
    abogado = models.ForeignKey(Abogado, related_name='casos', on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, related_name='casos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipos_casos = models.CharField(max_length=10, default='Penal', choices=CASOS_CHOICES)
    Estado = models.CharField(max_length=10, default='Proceso', choices=ESTADO_CHOICES)
    fecha_apertura = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'Caso: {self.nombre} - Abogado: {self.abogado.nombrea} - Cliente: {self.cliente.nombrec}'

    def get_absolute_url(self):
        return reverse('ver_caso', kwargs={'codigo_caso': self.pk})
    def get_edit_url(self):
        return reverse('editar_caso', kwargs={'codigo_caso': self.pk})
    
    def get_delete_url(self):
        return reverse('eliminar_caso', kwargs={'codigo_caso': self.pk})  
        
class Documentos(models.Model):
    # Atributos del documento
    caso = models.ForeignKey(Casos, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion_documento = models.TextField()
    archivo_adjunto = models.FileField(upload_to='documentos/', blank=True, )

    def __str__(self) -> str:
        return f'Documento {self.tipo_documento} - Abogado: {self.caso.abogado.nombrea} - Cliente: {self.caso.cliente.nombrec}'
    


    def get_absolute_url(self):
        return reverse('ver_documento', kwargs={'codigo_documento': self.pk})
    
    def get_edit_url(self):
        return reverse('editar_documento', kwargs={'codigo_documento': self.pk})
    
    def get_delete_url(self):
        return reverse('eliminar_documento', kwargs={'codigo_documento': self.id})  
    


    
class Info_Abogado(models.Model):
    abogado = models.ForeignKey(Abogado, related_name='info', on_delete=models.CASCADE, null=True,)
    descripcion = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.abogado.nombrea        