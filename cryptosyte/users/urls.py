from django.urls import path
from users import views

urlpatterns = [
 path('login/', views.LoginUser.as_view(), name='login'),
 path('logout/', views.logout_user, name='logout'),
 path('register/', views.RegisterUser.as_view(), name='register'),
 path('profile/<int:pk>/', views.ProfileUser.as_view(),name='profile'),
]

app_name = "users"