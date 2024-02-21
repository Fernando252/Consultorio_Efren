from django.urls import path
from e_mail import views
from login.views import editar_cita,subir_documento,registro_cliente, registrar_cita,CitaListView,citas_t,ver_cita,eliminar_cita
urlpatterns = [
    #email
    path('inbox',views.InboxView.as_view(),name='email-inbox'),
    path('emailread',views.EmailReadView.as_view(),name='email-emailread'),
    path('emailcompose',views.EmailComposeView.as_view(),name='email-emailcompose'),
    path('subir_documento/', subir_documento, name='subir_documento'),
    path('registro_cliente/', registro_cliente, name='registro_cliente'),
  
    path('registrar_cita1/', registrar_cita, name='registrar_cita1'),
    path('citas/', CitaListView.as_view(), name='citas_list'),
    
    path('lista_citas/', citas_t,name="lista_citas"),
    path('cita/<int:codigo_cita>/', ver_cita, name='ver_cita'),
    path('eliminar_cita/<int:codigo_cita>/', eliminar_cita, name='eliminar_cita'),
    path('editar_cita/<int:codigo_cita>/',editar_cita, name='editar_cita'),
]