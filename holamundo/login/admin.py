from django.contrib import admin
from .models import  Abogado, Clientes, Cita, Casos, Documentos

class Abogadoadmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Abogado)
class AbogadoAdmin(admin.ModelAdmin):
    list_display = ('nombrea', 'apellido', 'celular', 'correo','tipos_especialidad')
    search_fields = ('apellido','tipos_especialidad')

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nombrec', 'apellido', 'direccion', 'celular', 'correo')
    search_fields = ('nombrec', 'apellido', 'direccion', 'celular',)

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('abogado', 'cliente', 'fecha_cita', 'lugar_cita', 'descripcion', 'fecha_creacion')
    list_filter = ('abogado', 'cliente', 'fecha_cita')
    search_fields = ('abogado__nombrea', 'cliente__nombrec', 'lugar_cita', 'descripcion')

@admin.register(Casos)
class CasosAdmin(admin.ModelAdmin):
    list_display = ('abogado', 'cliente', 'tipos_casos', 'Estado', 'fecha_apertura', 'descripcion')
    list_filter = ('tipos_casos', 'Estado')
    search_fields = ('abogado__nombrea', 'cliente__nombrec')


@admin.register(Documentos)
class DocumentosAdmin(admin.ModelAdmin):
    list_display = ('caso', 'tipo_documento', 'fecha_creacion', 'archivo_adjunto')
    list_filter = ('caso', 'tipo_documento')
    search_fields = ('caso__cliente__nombre', 'tipo_documento', 'fecha_creacion')
