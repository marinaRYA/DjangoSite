from django.urls import reverse
class DataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')  # URL для главной страницы
        context['markets_url'] = reverse('markets')  # URL для страницы рынков
        context['trade_url'] = reverse('trade')  # URL для списка постов4e
        if self.request.user.is_authenticated:
            context['profile_url'] = reverse('users:profile', kwargs={'pk': self.request.user.pk})
        else:
            context['profile_url'] = '#'
        return context