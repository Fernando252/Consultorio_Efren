from django.http import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView, PasswordSetView
from django.contrib.auth.mixins import LoginRequiredMixin 



class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        greeting = {}
        greeting['title'] = "Dashboard"
        greeting['heading'] = "consultorio" 
        greeting['subheading'] = "Dashboard" 
        return render(request, 'dashboard.html',greeting)


 
class MyPasswordChangeView( PasswordChangeView):
    success_url = reverse_lazy('dashboard')


class MyPasswordSetView( PasswordSetView):
    success_url = reverse_lazy('dashboard')