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
<<<<<<< HEAD
from login.views import ver_perfil_usuario,editar_documento,nueva_docu,eliminar_documento,ver_documento,ver_documentos,ver_cita,citas_t,CitaListView,registrar_cita, ver_casos,casos_abogado,registro_abogado, registro_cliente, subir_documento, nueva_cita, eliminar_cita, editar_cita
=======
from login.views import ver_abogados,editar_documento,nueva_docu,eliminar_documento,ver_documento,ver_documentos,ver_cita,citas_t,CitaListView,registrar_cita, ver_casos,casos_abogado,registro_abogado, registro_cliente, subir_documento, nueva_cita, eliminar_cita, editar_cita
>>>>>>> 9df5c5659f762e91caf18569588ed7e9675cdf5f
from consultorio import views
from django.contrib.auth.decorators import login_required
from .views import MyPasswordChangeView, MyPasswordSetView


urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('mi_perfil/',ver_perfil_usuario,name='ver_perfil_usuario'),
    path('accounts/profile',ver_perfil_usuario,name='ver_perfil_usuario'),

    path('citas/', CitaListView.as_view(), name='citas_list'),
    path('registrar_cita/', registrar_cita, name='registrar_cita'),

    path('editar_cita/<int:codigo_cita>/',editar_cita, name='editar_cita'),

    path('lista_citas/', citas_t,name="lista_citas"),
    path('cita/<int:codigo_cita>/', ver_cita, name='ver_cita'),
    path('eliminar_cita/<int:codigo_cita>/', eliminar_cita, name='eliminar_cita'),
  

    path('registrar_cita1/', nueva_cita, name='registrar_cita1'),
    path('registro_cliente/', registro_cliente, name='registro_cliente'),
    path('registro_abogado/', registro_abogado, name='registro_abogado'),
    path('lista_abogados/', ver_abogados,name="lista_abogados"),

    path('subir_documento/', subir_documento, name='subir_documento'),
    path('lista_documentos/', ver_documentos,name="lista_documentos"),
    path('documento/<int:codigo_documento>/', ver_documento, name='ver_documento'),
    path('eliminar_documento/<int:codigo_documento>/', eliminar_documento, name='eliminar_documento'),
    path('edit_documento/', nueva_docu, name='nueva_docu'),
    path('editar_documento/<int:codigo_documento>/',editar_documento, name='editar_documento'),

    path('ver_casos/', ver_casos, name='ver_casos'),
    path('caso/<int:codigo_abogado>/', casos_abogado, name="detalle_casos"),
       

       
    path('calendar', views.CalendarView.as_view(), name='calendar'),
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
   
    

]