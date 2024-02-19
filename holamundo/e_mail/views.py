from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class InboxView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['title'] = "Documento"
        greeting['heading'] = "consultorio"
        greeting['subheading'] = "Email"
        return render (request,'subir_documento.html',greeting)

class EmailReadView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['title'] = "Email Read"
        greeting['heading'] = "consultorio"
        greeting['subheading'] = "Email"
        return render (request,'email/email-emailread.html',greeting)          

class EmailComposeView(LoginRequiredMixin,View):
    def get(self , request):
        greeting = {}
        greeting['title'] = "Email Compose"
        greeting['heading'] = "consultorio"
        greeting['subheading'] = "Email"
        return render (request,'email/email-emailcompose.html',greeting)          