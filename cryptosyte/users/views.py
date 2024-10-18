from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from users.models import Profile
from crypto.models import Comment
from crypto.utils import DataMixin

class LoginUser(LoginView):
 template_name = 'users/login.html'
 extra_context = {'title': "Авторизация"}
 form_class = AuthenticationForm

 def get_success_url(self):
  return self.get_redirect_url() or reverse_lazy('home')


def logout_user(request):
 logout(request)
 return HttpResponseRedirect(reverse('home'))

class RegisterUser(CreateView):
 form_class = RegisterUserForm
 template_name = 'users/register.html'
 extra_context = {'title': "Регистрация"}
 success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, DataMixin, UpdateView):
    model = get_user_model()  # Указывает на модель пользователя
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        # Получаем профиль пользователя
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем информацию о пользователе
        user = self.request.user
        context['user'] = user

        # Добавляем профиль пользователя
        profile = self.get_object()
        context['profile'] = profile

        # Добавляем комментарии пользователя
        user_comments = Comment.objects.filter(user=user)  # Замените Comment на вашу модель комментариев
        context['user_comments'] = user_comments
        context['comment_count'] = user_comments.count()

        return context

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}