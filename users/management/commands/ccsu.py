from getpass import getpass

from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    ccsu - custom create super user.
    """
    help = 'Create a superuser with a custom email and password'

    def add_arguments(self, parser):
        """
        Можно передать аргументы как флаги сразу с функцией,
        или ввести их потом
        """
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def validate_email(self, email):
        """
        Валидация email (такая же, как models.EmailField)
        """
        try:
            User._meta.get_field('email').run_validators(email)
        except ValidationError as e:
            raise ValidationError(f'Email validation error: {e}')

    def validate_password(self, password):
        """
        Валидация password (такая же, как у AbstractBaseUser)
        """
        try:
            User._meta.get_field('password').run_validators(password)
        except ValidationError as e:
            raise ValidationError(f'Password validation error: {e}')

    def handle(self, *args, **options):
        # Получение через **options данных, либо их input
        email = options['email'] or input('Enter admin email or "exit": ')
        password = options['password'] or getpass('Enter admin password or "exit": ')

        while True:
            # Выход из цикла в случае ввода 'exit' в любом регистре
            if email.lower() == 'exit' or password.lower() == 'exit':
                print("User creation canceled!")
                break

            # Валидация email и password
            try:
                self.validate_email(email)
                self.validate_password(password)
            except ValidationError as e:
                print(e)
                continue

            # Подтверждение пароля через невидимый input(через getpass)
            confirm_password = getpass('Confirm admin password: ')

            # Сравнение паролей
            if password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")

        # Создание супер-пользователя
        if email.lower() != 'exit' and password.lower() != 'exit':
            user = User.objects.create(
                email=email,
                first_name='Admin',
                last_name='Admin',
                is_staff=True,
                is_active=True,
                is_superuser=True
            )

            user.set_password(password)
            user.save()
            print('A new superuser has been created!')
