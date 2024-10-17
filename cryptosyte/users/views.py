from django.contrib.auth import logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterUserForm, ProfileUserForm
from users.models import Profile
from crypto.models import Comment
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



class ProfileUser(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        # Добавляем данные профиля в контекст
        context['profile'] = profile
        context['bio'] = profile.bio
        context['location'] = profile.location
        context['birth_date'] = profile.birth_date

        # Добавляем комментарии пользователя
        user_comments = Comment.objects.filter(user=self.request.user)  # Замените Comment на вашу модель
        context['user_comments'] = user_comments
        context['comment_count'] = user_comments.count()

        return context
