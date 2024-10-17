from django.contrib.auth.models import User
from django.db import models
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

class Currency(models.TextChoices):
    USD = 'USD', 'Доллар США'
    EUR = 'EUR', 'Евро'
    RUB = 'RUB', 'Российский рубль'


class ActualCurrency(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Crypto(models.Model):
    currency = models.CharField(max_length=3, choices=Currency.choices, verbose_name="Валюта")
    name = models.CharField(max_length=10, verbose_name="Название")
    price = models.FloatField(verbose_name="Цена")
    time_lastupdate = models.DateTimeField(auto_now=False, verbose_name="Последнее обновление")
    slug = models.SlugField(unique=True, verbose_name="Слаг")

    objects = models.Manager()
    actual_crypto = ActualCurrency()

    class Meta:
        verbose_name = "Криптовалюта"
        verbose_name_plural = "Криптовалюты"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тега")
    posts = models.ManyToManyField(Post, related_name='tags', verbose_name="Записи")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name="Запись")
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField(blank=True, null=True, verbose_name="Комментарий")  # Делаем поле необязательным
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', default=None, blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.content or "Комментарий без текста"

    def clean(self):
        if not self.content and not self.image:
            raise ValidationError('Необходимо заполнить хотя бы одно поле: комментарий или изображение.')

    def save(self, *args, **kwargs):
        # Сжатие изображения
        if self.image:
            img = PilImage.open(self.image)

            # Проверяем размеры изображения
            max_size = (100, 100)
            img.thumbnail(max_size, PilImage.LANCZOS)  # Используем LANCZOS вместо ANTIALIAS

            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=100)
            img_file = ContentFile(img_io.getvalue(), name=self.image.name)
            self.image = img_file

        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

