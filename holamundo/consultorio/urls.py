"""consultorio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#clientes_documentos
from login.views import ver_documentos,eliminar_documento,editar_documento,ver_documento,lista_abogados_con_horario,registrar_cita
#clientes_casos
from login.views import abogados_por_cliente,ver_casos_abogado
#Perfil_abogado
from login.views import ver_abogados,detalle_abogado,ver_cliente_usuario,clientesviews
#________________________________________________________________________________________________
#abogados_casos
from login.views import registrar_caso, clientes_con_casos, ver_casos_cliente, abogado_ver_caso, editar_caso_abogado,eliminar_caso
#abogados_documentos
from login.views import abogado_subir_documento,abogado_ver_documentos,abogado_ver_casos_cliente, ver_documentos_caso,editar_documento_abogado,eliminar_documento_abogado
#Perfil abogado
from login.views import ver_abogado,editar_abogado
#Citas
from login.views import registrar_horario,lista_clientes_citas_abogado,citas_cliente_con_abogado,lista_fechas_horarios_abogado,horarios_en_fecha


from consultorio import views
from django.contrib.auth.decorators import login_required
from .views import MyPasswordChangeView, MyPasswordSetView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    
  
    path('admin/', admin.site.urls),
    path('accounts/profile/', ver_cliente_usuario, name='profile'),
    path('', views.DashboardView.as_view(), name='dashboard'),

    #documentos 
    path('lista_documentos/', ver_documentos,name="lista_documentos"),
    path('eliminar_documento/<int:codigo_documento>/', eliminar_documento, name='eliminar_documento'),
    path('editar_documento/<int:codigo_documento>/',editar_documento, name='editar_documento'),
    path('documento/<int:codigo_documento>/', ver_documento, name='ver_documento'),
    #casos 
    path('abogados_por_cliente/', abogados_por_cliente, name='abogados_por_cliente'),
    path('caso/<int:codigo_abogado>/', ver_casos_abogado, name="detalle_casos"),
    
    #Perfil abogado
    path('lista_abogados/', ver_abogados,name="lista_abogados"),
    path('detalle_abogado/<int:codigo_abogado>/', detalle_abogado, name='detalle_abogado'),
    

    #abogados 
#______________________________________________________________________________________
    # Ver casos por cliente en vista abogado    
    path('registrar_caso/', registrar_caso, name='registrar_caso'),
    path('clientes_con_casos/', clientes_con_casos, name='clientes_con_casos'),
    path('ver_casos_cliente/<int:cliente_id>/', ver_casos_cliente, name='ver_casos_cliente'),
    #Mas detalle 
    path('abogado_caso_cliente/<int:codigo_caso>/', abogado_ver_caso, name='abogado_ver_caso'),
    #Editar vista abogado caso
    path('editar_caso_abogado/<int:codigo_caso>/', editar_caso_abogado, name='editar_caso_abogado'),
    #Eliminar caso vista abogado
   path('eliminar_caso/<int:codigo_caso>/', eliminar_caso, name='eliminar_caso'),
#______________________________________________________________________________________

    #Perfil abogado
    path('ver_abogado/', ver_abogado, name='ver_abogado'),
    path('editar_abogado/<int:codigo_abogado>/', editar_abogado, name='editar_abogado'),
#______________________________________________________________________________________
    #Documentos 
    path('subir_documento/', abogado_subir_documento, name='abogado_subir_documento'),
    path('lista_clientes/', abogado_ver_documentos, name='ver_documentos_abogado'),
    path('casos_cliente/<int:cliente_id>/', abogado_ver_casos_cliente, name='documento_casos_cliente'),
    path('ver_documentos_caso/<int:caso_id>/', ver_documentos_caso, name='ver_documentos_caso'),
    path('editar_documento_abogado/<int:codigo_documento>/',editar_documento_abogado, name='editar_documento_abogado'),
    path('eliminar_documento_abogado/<int:codigo_documento>/', eliminar_documento_abogado, name='eliminar_documento_abogado'),
#______________________________________________________________________________________
    #Citas
    path('registrar_horario/', registrar_horario, name='registrar_horario'),
    path('abogados_con_horario/', lista_abogados_con_horario, name='abogados_con_horario'),
    path('registrar_cita_abogado/<int:abogado_id>/', registrar_cita, name='registrar_cita_abogado'),
    path('lista_clientes_citas_abogado/', lista_clientes_citas_abogado, name='lista_clientes_citas_abogado'),
    path('citas_cliente_con_abogado/<int:abogado_id>/', citas_cliente_con_abogado, name='citas_cliente_con_abogado'),
    path('lista_fechas_horarios_abogado/', lista_fechas_horarios_abogado, name='lista_fechas_horarios_abogado'),
    path('horarios_en_fecha/<str:fecha>/', horarios_en_fecha, name='horarios_en_fecha'),

    # Email
    path("email/", include("e_mail.urls")),
    # Components
    path("components/", include("components.urls")),
    # Extra_Pages
    path("extra_pages/", include("extra_pages.urls")),
    # Extra_Pages
    path("email_templates/", include("email_templates.urls")),
    # layouts
    path("layouts/", include("layouts.urls")),
    path("authentication/", include("authentication.urls")),

    path(
        "account/password/change/",
        login_required(MyPasswordChangeView.as_view()),name="account_change_password",),
    path(
        "account/password/set/",
        login_required(MyPasswordSetView.as_view()),name="account_set_password",),
 
    path('accounts/', include('allauth.urls')),
   
   path('extraer_clientes/', clientesviews, name='extraer_clientes')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)