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


from login.views import editar_documento_abogado,eliminar_caso,editar_caso_abogado,abogado_ver_caso,ver_documentos,ver_documento,abogado_ver_documentos,abogado_ver_casos_cliente,clientes_con_casos
from login.views import clientesviews, detalle_abogado, ver_cliente_usuario,abogado_subir_documento,ver_casos_cliente,ver_documentos_caso

from login.views import registrar_caso,abogados_por_cliente,ver_abogados,editar_documento,eliminar_documento,ver_casos_abogado, editar_abogado, ver_abogado


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
    path('eliminar_documento_abogado/<int:codigo_documento>/', eliminar_documento, name='eliminar_documento_abogado'),


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