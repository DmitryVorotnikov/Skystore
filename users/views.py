import secrets
import string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, RedirectView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class LogoutUserView(LoginRequiredMixin, LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        # Сохранение в оперативную память (без добавление в БД)
        user = form.save(commit=False)
        # Пользователь неактивен, пока не подтвердит email
        user.is_active = False
        # Генерируем токен, через secrets, и сохраняет его в поле пользователя
        user.confirmation_token = secrets.token_urlsafe(30)
        user.save()

        # Создаем ссылку с токеном на следующий контроллер-представление
        verification_link = self.request.build_absolute_uri(
            reverse_lazy('users:verify_email', kwargs={'token': user.confirmation_token}),
        )

        # Отправляем письмо с ссылкой-токеном
        send_mail(
            subject='Верификация аккаунта',
            message=f'Осталось только подтвердить ваш аккаунт, перейдя по ссылке: {verification_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class VerifyEmailView(RedirectView):
    # Устанавливает перенаправление как временное (а не постоянное)
    permanent = False
    # Устанавливает сохранение параметров запроса и включение их в целевой URL после перенаправления
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        # Получает токен из URL
        token = kwargs.get('token')
        try:
            # Ищет по токену пользователя с таким же токеном
            user = User.objects.get(confirmation_token=token)
            # Активация пользователя
            user.is_active = True
            # Удаление токена из поля пользователя (опционально)
            user.confirmation_token = ''
            user.save()
            return reverse('users:login')
        except User.DoesNotExist:
            print('Неверный токен')
            # Если токен неверный или истек, можно перенаправить на страницу с ошибкой
            return reverse('users:login')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('catalog:home')

    # Что бы не пришлось на страницу профиля передавать pk
    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            # Проверка что выбран чекбокс "need_generate"
            if form.data.get('need_generate', False):
                # Генерация нового пароля (с помощью secrets и string) и присваивание пользователю
                new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
                self.object.set_password(new_password)
                self.object.save()

                # Отправка нового пароля на почту пользователя
                send_mail(
                    subject='Вы сменили пароль',
                    message=f'Ваш новый пароль: {new_password}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[self.object.email],
                )

        return super().form_valid(form)
