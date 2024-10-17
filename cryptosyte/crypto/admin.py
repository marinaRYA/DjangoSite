from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Crypto, Post, Tag, Comment, Profile
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta, datetime

admin.site.site_header = "Моя Админ-Панель"
admin.site.site_title = "Портал Администрирования"
admin.site.index_title = "Добро пожаловать в Мою Админ-Панель"


@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency', 'price', 'time_lastupdate', 'slug')

    @admin.display(description="Название")
    def name_display(self, obj):
        return obj.name

    @admin.display(description="Валюта")
    def currency_display(self, obj):
        return obj.currency

    @admin.display(description="Цена")
    def price_display(self, obj):
        return obj.price

    @admin.display(description="Последнее обновление")
    def time_lastupdate_display(self, obj):
        return obj.time_lastupdate

    @admin.display(description="Слаг")
    def slug_display(self, obj):
        return obj.slug
    search_fields = ('name', 'currency')
    list_filter = ('currency',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

    @admin.display(description="Название")
    def name_display(self, obj):
        return obj.name
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    list_filter = ('created_at', 'title')

    # Пользовательские действия
    actions = ['delete_old_posts']

    def delete_old_posts(self, request, queryset):
        # Находим посты, которым больше года
        one_year_ago = timezone.now() - timedelta(days=365)
        old_posts = queryset.filter(created_at__lt=one_year_ago)

        count = old_posts.count()
        old_posts.delete()
        self.message_user(request, f"{count} пост(а) старше года успешно удалено.")

    delete_old_posts.short_description = "Удалить посты старше года"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    @admin.display(description="Изображение")
    def post_image(self, comment: Comment):
        if comment.image:
            return mark_safe(f"<img src='{comment.image.url}'width=50>")
        return "Без фото"

    list_display = ('post', 'user', 'content', 'post_image', 'created_at')
    search_fields = ('content',)
    list_filter = ('post', 'user')

    # Пользовательские действия
    actions = ['delete_selected_comments']
    def delete_selected_comments(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} комментариев успешно удалено.")
    delete_selected_comments.short_description = "Удалить выбранные комментарии"





@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date', 'age','days_until_birthday' )
    search_fields = ('user__username', 'bio')
    list_filter = ('location',)

    def age(self, obj):
        if obj.birth_date:
            return (timezone.now().date() - obj.birth_date).days // 365
        return None

    age.admin_order_field = 'birth_date'
    age.short_description = 'Возраст'
    def days_until_birthday(self, obj):
        if obj.birth_date:
            today = timezone.now().date()
            next_birthday = datetime(today.year, obj.birth_date.month, obj.birth_date.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, obj.birth_date.month, obj.birth_date.day).date()
            days_remaining = (next_birthday - today).days
            return days_remaining
        return "Нет даты"

    days_until_birthday.admin_order_field = 'birth_date'  # Указывает на поле для сортировки
    days_until_birthday.short_description = 'Дней до дня рождения'  # Описание для заголовка столбца

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, "Запись успешно сохранена.")