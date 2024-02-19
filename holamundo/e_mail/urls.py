from django.urls import path
from e_mail import views
from login.views import subir_documento,registro_cliente,ver_casos, registrar_cita,CitaListView
urlpatterns = [
    #email
    path('inbox',views.InboxView.as_view(),name='email-inbox'),
    path('emailread',views.EmailReadView.as_view(),name='email-emailread'),
    path('emailcompose',views.EmailComposeView.as_view(),name='email-emailcompose'),
    path('subir_documento/', subir_documento, name='subir_documento'),
    path('registro_cliente/', registro_cliente, name='registro_cliente'),
    path('ver_casos/', ver_casos, name='ver_casos'),
    path('registrar_cita/', registrar_cita, name='registrar_cita'),
    path('citas/', CitaListView.as_view(), name='citas_list'),
]