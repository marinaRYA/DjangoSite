from django.urls import reverse
class DataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = reverse('home')  # URL для главной страницы
        context['markets_url'] = reverse('markets')  # URL для страницы рынков
        context['trade_url'] = reverse('trade')  # URL для списка постов4e
        # Добавьте другие URL по необходимости
        return context