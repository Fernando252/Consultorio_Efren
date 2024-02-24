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

from login.views import ver_documentos
from login.views import clientesviews, detalle_abogado, ver_cliente_usuario
from login.views import registrar_caso,abogados_por_cliente,ver_abogados,editar_documento,eliminar_documento,ver_documento,ver_casos_abogado, editar_abogado


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
    path('caso/<int:codigo_abogado>/', ver_casos_abogado, name="detalle_casos"),
    path('eliminar_documento/<int:codigo_documento>/', eliminar_documento, name='eliminar_documento'),
    path('editar_documento/<int:codigo_documento>/',editar_documento, name='editar_documento'),

    #casos 
    path('lista_abogados/', ver_abogados,name="lista_abogados"),

    path('editar_abogado/<int:codigo_abogado>/', editar_abogado, name='editar_abogado'),

    path('abogados_por_cliente/', abogados_por_cliente, name='abogados_por_cliente'),
    path('caso/<int:codigo_abogado>/', ver_casos_abogado, name="detalle_casos"),
    
    #Perfil abogado
    path('detalle_abogado/<int:codigo_abogado>/', detalle_abogado, name='detalle_abogado'),
    path('editar_abogado/<int:codigo_abogado>/', editar_abogado, name='editar_abogado'),

    #Casos
    path('registrar_caso/', registrar_caso, name='registrar_caso'),

    
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