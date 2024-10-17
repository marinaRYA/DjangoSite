from django import forms
from django.core.exceptions import ValidationError
from .models import Comment

# Форма, не связанная с моделью
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя")
    email = forms.EmailField(label="Ваш email")

    # Собственный валидатор для имени
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError('Имя должно быть не менее 3 символов.')
        return name

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')

        if content:
            if len(content) > 200:
                raise ValidationError('Комментарий должен содержать не более 200 символов.')

        return cleaned_data



