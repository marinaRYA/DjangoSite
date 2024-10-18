import requests
from datetime import datetime
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView, UpdateView
from .utils import DataMixin
from .models import Crypto, Post, Tag, Comment
from .forms import ContactForm, CommentForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
def format_date(date):
    return date.strftime('%d.%m.%y')


class BaseContextMixin(DataMixin):
    """Mixin to add common context data to views."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['comments'] = Comment.objects.all()
        return context


class HomeView(TemplateView):
    template_name = "home.html"

# class ProfileDetailView(LoginRequiredMixin, BaseContextMixin, DetailView):
#     model = Profile
#     template_name = 'profile.html'
#     context_object_name = 'profile'
#
#     def get_object(self, queryset=None):
#         # Возвращаем профиль текущего пользователя
#         return self.request.user.profile
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         user = self.request.user
#
#
#         # Получаем все комментарии пользователя
#         user_comments = Comment.objects.filter(user=user)
#
#         # Количество комментариев пользователя
#         comment_count = user_comments.count()
#
#
#         context['user_comments'] = user_comments
#         context['comment_count'] = comment_count
#
#         return context

class CurrencyDetailView(DetailView):
    model = Crypto
    template_name = 'currencies.html'
    slug_field = 'slug'
    slug_url_kwarg = ('currencies_slug'
                      '')


class ArchiveView(BaseContextMixin, TemplateView):
    template_name = 'archive.html'  # Update with your actual template name

    def get(self, request, currency_name, year):
        year = int(year)
        if 2018 <= year <= 2024:
            return HttpResponse(f"<h1>Archive</h1><p>Currency: {currency_name}, Year: {year}</p>")
        else:
            return redirect(reverse('invalid_year', args=(currency_name, year)))


class InvalidYearView(BaseContextMixin, TemplateView):
    template_name = 'invalid_year.html'  # Update with your actual template name

    def get(self, request, currency_name, year):
        return HttpResponse(f"<h1>Error</h1><p>Invalid year: {year}</p>")



class TradeView(BaseContextMixin, TemplateView):
    template_name = 'trade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = self.request.GET.get('start_date', datetime.now().strftime('%Y-%m-%d'))

        cryptocurrencies = Crypto.actual_crypto.filter(time_lastupdate__date=selected_date)

        if not cryptocurrencies.exists():
            success = self.fetch_and_update_crypto_data(selected_date)
            if success:
                cryptocurrencies = Crypto.actual_crypto.filter(time_lastupdate__date=selected_date)

        average_prices = Crypto.objects.values('name').annotate(average_price=Avg('price'))
        average_prices_dict = {item['name']: item['average_price'] for item in average_prices}

        context['cryptocurrencies'] = cryptocurrencies
        context['average_prices'] = average_prices_dict
        context['today'] = datetime.today().strftime('%Y-%m-%d')
        return context

    def fetch_and_update_crypto_data(self, selected_date):
        base_url = f"https://api.coinlayer.com/api/{selected_date}"
        access_key = '92f9b1a42efd0698272de40ff217a872'
        symbols = 'BTC,ETH,XRP'
        targets = ['USD', 'EUR', 'RUB']

        success = True

        for target in targets:
            params = {
                'access_key': access_key,
                'symbols': symbols,
                'target': target
            }
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    for symbol in symbols.split(','):
                        price = data['rates'][symbol]
                        Crypto.objects.update_or_create(
                            slug=f"{symbol}#{selected_date}#{target}",
                            defaults={
                                'name': symbol,
                                'price': price,
                                'currency': target,
                                'time_lastupdate': selected_date,
                            }
                        )
                else:
                    success = False
            else:
                success = False

        return success


class PostListView(LoginRequiredMixin, BaseContextMixin, ListView):
    model = Post
    template_name = 'markets.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.request.GET.get('tag')
        context['selected_tag'] = int(tag_id) if tag_id else None

        # Фильтруем посты по тегу, если выбран
        posts = Post.objects.filter(tags__id=tag_id) if tag_id else Post.objects.all()

        # Настройка пагинации
        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        context['page'] = paginator.get_page(page_number)  # Добавляем объект страницы в контекст
        context['form'] = CommentForm()  # Добавляем новую форму для комментариев
        context['total_posts'] = posts.count()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # Проверяем, авторизован ли пользователь
            form = CommentForm(request.POST, request.FILES)  # Обработка файлов
            if form.is_valid():
                comment = form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = get_object_or_404(Post, id=post_id)  # Убедимся, что пост существует
                comment.post = post  # Привязываем комментарий к посту
                comment.user = request.user  # Устанавливаем автора комментария как авторизованного пользователя
                comment.save()  # Сохраняем комментарий
                return redirect('markets')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Ошибка: {error}")
        else:
            messages.warning(request, "Пожалуйста, войдите в систему, чтобы оставить комментарий.")

        return redirect('markets')

class ContactView(BaseContextMixin, FormView):
    form_class = ContactForm
    template_name = 'contact_form.html'

    def form_valid(self, form):
        # Здесь можно добавить логику отправки данных, например, по email
        response_data = {
            'status': 'success',
            'message': f'Спасибо, {form.cleaned_data["name"]}! Ваше сообщение отправлено.'
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):

        response_data = {
            'status': 'error',
            'errors': form.errors.as_json()
        }
        return JsonResponse(response_data)


class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'confirm_delete.html'  # Убедитесь, что у вас есть этот шаблон
    success_url = reverse_lazy('markets')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'comment_update.html'

    def get_success_url(self):
        return reverse('markets', kwargs={'post_id': self.object.post.id})


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем пользователя и профиль
            return redirect('login')  # Перенаправляем на страницу входа или другую
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})