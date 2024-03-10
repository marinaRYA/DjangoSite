"""
URL configuration for cryptosyte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
#from django.contrib import admin
from django.urls import path
from crypto import views

handler404 = 'crypto.views.page_not_found'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home),
    path('trade', views.trade, name='trade'),
    path('markets', views.markets, name='markets'),
    path('currencies/<str:currency_name>/', views.currencies, name='currencies'),
    path('currencies/<str:currency_name>/<int:year>/', views.archive, name='archive'),
    path('currencies/<str:currency_name>/<int:year>/invalid_year/', views.invalid_year, name='invalid_year'),
]
