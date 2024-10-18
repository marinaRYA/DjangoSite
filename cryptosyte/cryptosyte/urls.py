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
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from crypto import views

handler404 = 'crypto.views.page_not_found'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('currencies/<slug:currencies_slug>/', views.CurrencyDetailView.as_view(), name='currencies'),
    path('archive/<str:currency_name>/<int:year>/', views.ArchiveView.as_view(), name='archive'),
    path('invalid-year/<str:currency_name>/<int:year>/', views.InvalidYearView.as_view(), name='invalid_year'),
    path('trade/', views.TradeView.as_view(), name='trade'),
    path('markets/', views.PostListView.as_view(), name='markets'),
    path('contact/', views.ContactView.as_view(), name='contact_form'),
    path('delete_comment/<int:pk>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('markets/<int:post_id>/', views.PostListView.as_view(), name='markets'),
    path('users/', include('users.urls', namespace='users'))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
