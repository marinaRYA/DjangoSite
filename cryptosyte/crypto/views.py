from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Crypto
def home(request):
    return render(request, "home.html")

def markets(request):
    return render(request, "markets.html")


def currencies(request, currencies_slug):
    # Получаем объект Crypto по slug
    crypto = get_object_or_404(Crypto, slug=currencies_slug)

    # Передаем объект Crypto в шаблон для отображения
    return render(request, 'currencies.html', {'crypto': crypto})



def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")

def archive(request, currency_name, year):
    year = int(year)
    if 2009 <= year <= 2024:
        # Показываем обычную страницу архива
        return HttpResponse(f"<h1>Archive</h1><p>Currency: {currency_name}, Year: {year}</p>")
    else:
        # Если год не входит в допустимый диапазон, перенаправляем пользователя на другую страницу
        return redirect(reverse('invalid_year', args=(currency_name, year)))

def invalid_year(request, currency_name, year):
    return HttpResponse(f"<h1>Error</h1><p>Invalid year: {year}</p>")


def get_crypto_prices():
    # Получаем все объекты модели Crypto из базы данных
    cryptocurrencies = Crypto.objects.all()

    # Преобразуем объекты модели в словари, чтобы сохранить структуру данных как в вашем примере
    crypto_data = [{'name': crypto.name, 'price': crypto.price} for crypto in cryptocurrencies]

    return crypto_data

def trade(request):
    # Получаем список криптовалют и их цен
    cryptocurrencies = get_crypto_prices()

    # Передаем криптовалюты и их цены в шаблон
    return render(request, 'trade.html', {'cryptocurrencies': cryptocurrencies})
