from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse
def home(request):
    return render(request, "home.html")

def markets(request):
    return render(request, "markets.html")

def currencies(request, currency_name):
    return HttpResponse(f"<h1>Currencies</h1><p>Name: {currency_name}</p>")



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
    # список криптовалют с ценами
    cryptocurrencies = [
        {'name': 'Bitcoin', 'price': 67777},
        {'name': 'Ethereum', 'price': 3861},
        {'name': 'Litecoin', 'price': 87},
    ]
    return cryptocurrencies

def trade(request):
    # Получаем список криптовалют и их цен
    cryptocurrencies = get_crypto_prices()

    # Передаем криптовалюты и их цены в шаблон
    return render(request, 'trade.html', {'cryptocurrencies': cryptocurrencies})
