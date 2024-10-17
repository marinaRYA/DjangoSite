from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from users import views

urlpatterns = [
 path('login/', views.LoginUser.as_view(), name='login'),
 path('logout/', views.logout_user, name='logout'),
 path('register/', views.RegisterUser.as_view(), name='register'),
 path('profile/<int:pk>/', views.ProfileUser.as_view(),name='profile'),
 path('password-change/', PasswordChangeView.as_view(), name='password_change'),
 path('password-change/done/',PasswordChangeDoneView.as_view(), name='password_change_done'),
path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
]

app_name = "users"