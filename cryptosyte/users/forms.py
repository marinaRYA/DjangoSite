from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from users.models import Profile
User = get_user_model()

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Биография")
    location = forms.CharField(max_length=255, required=False, label="Местоположение")
    birth_date = forms.DateField(
     required=False,
     widget=forms.SelectDateWidget(years=range(1950, 2024)),
     label="Дата рождения"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)  # Создаем экземпляр пользователя, но не сохраняем его
        if commit:
            user.save()  # Сохраняем пользователя
            Profile.objects.create(
                user=user,  # Присваиваем экземпляр пользователя, а не класс
                bio=self.cleaned_data['bio'],
                location=self.cleaned_data['location'],
                birth_date=self.cleaned_data['birth_date']
            )
        return user

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.CharField(
        disabled=True,
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    bio = forms.CharField(
        disabled=True,  # Поле только для чтения
        widget=forms.Textarea(attrs={'class': 'form-input'}),
        label='Биография',
        required=False
    )
    location = forms.CharField(
        disabled=True,  # Поле только для чтения
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        label='Местоположение',
        required=False
    )
    birth_date = forms.DateField(
        disabled=True,  # Поле только для чтения
        widget=forms.SelectDateWidget(years=range(1950, 2024)),
        label='Дата рождения',
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'location', 'birth_date']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }



