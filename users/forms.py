from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Скрытие лишних подсказок
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'country', 'avatar', 'need_generate')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Скрытие поля password
        self.fields['password'].widget = forms.HiddenInput()

        # Добавление чекбокса для need_generate
        self.fields['need_generate'].widget = forms.CheckboxInput()
