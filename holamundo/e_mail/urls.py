from django.urls import path
from e_mail import views
from login.views import subir_documento
urlpatterns = [
    #email
    path('inbox',views.InboxView.as_view(),name='email-inbox'),
    path('emailread',views.EmailReadView.as_view(),name='email-emailread'),
    path('emailcompose',views.EmailComposeView.as_view(),name='email-emailcompose'),

    
    path('subir_documento/', subir_documento, name='subir_documento'),
  
    
 
]