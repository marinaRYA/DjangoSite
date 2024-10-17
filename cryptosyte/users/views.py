from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy


class LoginUser(LoginView):
 template_name = 'users/login.html'
 extra_context = {'title': "Авторизация"}
 form_class = AuthenticationForm

 def get_success_url(self):
  return reverse_lazy('home')


def logout_user(request):
 logout(request)
 return HttpResponseRedirect(reverse('users:login'))
