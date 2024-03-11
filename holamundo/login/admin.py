from django.contrib import admin
from .models import  Abogado, Clientes, Casos, Documentos, Info_Abogado,Horario_atencion,Cita1


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


@admin.register(Casos)
class CasosAdmin(admin.ModelAdmin):
    list_display = ('abogado', 'cliente', 'tipos_casos', 'Estado', 'fecha_apertura', 'descripcion', 'historial_actualizaciones')
    list_filter = ('tipos_casos', 'Estado')
    search_fields = ('abogado__nombrea', 'cliente__nombrec')


@admin.register(Documentos)
class DocumentosAdmin(admin.ModelAdmin):
    list_display = ('caso', 'tipo_documento', 'fecha_creacion', 'archivo_adjunto')
    list_filter = ('caso', 'tipo_documento')
    search_fields = ('caso__cliente__nombre', 'tipo_documento', 'fecha_creacion')

@admin.register(Info_Abogado)
class Info_AbogadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'abogado', 'descripcion')
    list_filter = ('abogado',)

@admin.register(Horario_atencion)
class HorarioAtencionAdmin(admin.ModelAdmin):
    list_display = ('abogado', 'fecha', 'hora')
    list_filter = ('abogado', 'fecha', 'hora')
    search_fields = ('abogado__nombrea', 'fecha', 'hora')
   
@admin.register(Cita1)
class Cita1Admin(admin.ModelAdmin):
    list_display = ['cliente', 'horario_atencion', 'fecha_agendada']
    search_fields = ['cliente__username', 'horario_atencion__abogado__nombrea']  # Puedes personalizar esto según tus necesidades
    list_filter = ['fecha_agendada']