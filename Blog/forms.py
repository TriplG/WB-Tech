from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class SortAutorForm(forms.Form):
    sort_autor_form = forms.TypedChoiceField(label='Сортировать:',
                                       choices=[
                                           ('автор', 'По авторам'),
                                           ('количество', 'По количеству постов'),
                                           ]
                                       )


class SortHomeForm(forms.Form):
    sort_home_form = forms.TypedChoiceField(label='Сортировать:',
                                       choices=[
                                           ('Все', 'Все статьи'),
                                           ('Рекомендации', 'Рекомендации'),
                                           ('Прочитанные', 'Прочитанные'),
                                       ]
                                       )


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
