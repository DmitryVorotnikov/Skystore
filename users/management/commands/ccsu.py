from getpass import getpass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import BaseCommand
from django.core.validators import validate_email

from users.models import User


class Command(BaseCommand):
    """
    python manage.py ccsu - Custom Create SuperUser.
    """
    help = 'Custom Create SuperUser'

    def add_arguments(self, parser):
        """
        Можно передать аргументы как флаги сразу с командой или ввести их потом.

        You can pass arguments as flags directly with the command or enter them later.

        python manage.py ccsu

        --email=admin@example.com
        --password=example_password
        --confirm_password=example_password

        --first_name=Admin
        --last_name=Admin
        --is_active=True
        --is_staff=True
        --is_superuser=True
        """
        # Required
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--confirm_password', type=str, help='Confirm admin password')

        # Optional
        parser.add_argument('--first_name', type=str, help='first_name (default is "Admin")')
        parser.add_argument('--last_name', type=str, help='last_name (default is "Admin")')
        parser.add_argument('--is_active', type=str, help='is_active (default is "True")')
        parser.add_argument('--is_staff', type=str, help='is_staff (default is "True")')
        parser.add_argument('--is_superuser', type=str, help='is_superuser (default is "True")')

    @staticmethod
    def validate_email(email):
        """
        Валидация email (такая же, как AbstractUser).

        Email validation (same as AbstractUser).
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def validate_password(password):
        """
        Валидация password (такая же, как у AbstractBaseUser).

        Password validation (same as AbstractBaseUser).
        """
        try:
            validate_password(password)
            return True
        except ValidationError:
            return False

    def handle(self, *args, **options):
        # По умолчанию запрещено создание пользователя.
        # User creation is not required by default.
        user_creation_required = False

        # Получение email через **options, либо его input. Проверка и валидация.
        # Get email from **options or through input. Check and validate.
        email = options['email'] or input('Enter admin email or "exit":\n')

        if email.lower() == 'exit':
            print('User creation canceled!')
        elif not self.validate_email(email):
            print('Email validation error!')
        else:
            user_creation_required = True

        if user_creation_required:
            # Получение password через **options, либо его невидимый input (через getpass). Проверка и валидация.
            # Get password from **options or through a hidden input (using getpass). Check and validate.
            password = options['password'] or getpass('Enter admin password or "exit":\n')

            if password.lower() == 'exit':
                user_creation_required = False
                print('User creation canceled!')
            elif not self.validate_password(password):
                user_creation_required = False
                print('Password validation error!')

        if user_creation_required:
            # Получение confirm_password через **options, либо его невидимый input (через getpass).
            # Get confirm_password from **options or through a hidden input (using getpass).
            confirm_password = options['confirm_password'] or getpass('Confirm admin password:\n')
            if password != confirm_password:
                user_creation_required = False
                print('Passwords do not match. Please try again.')

        if user_creation_required:
            # Получение first_name, last_name, is_staff, is_active, is_superuser через **options, либо его input.
            # Get first_name, last_name, is_staff, is_active, is_superuser from **options or through input.
            first_name = options['first_name'] or input('Enter first_name (default is "Admin"):\n')
            last_name = options['last_name'] or input('Enter last_name (default is "Admin"):\n')
            is_active = options['is_active'] or input('Enter is_active (default is "True"):\n')
            is_staff = options['is_staff'] or input('Enter is_staff (default is "True"):\n')
            is_superuser = options['is_superuser'] or input('Enter is_superuser (default is "True"):\n')

            if not first_name or first_name == 'None':
                first_name = 'Admin'
            if not last_name or last_name == 'None':
                last_name = 'Admin'
            if not is_active.lower() == 'false':
                is_active = True
            if not is_staff.lower() == 'false':
                is_staff = True
            if not is_superuser.lower() == 'false':
                is_superuser = True

            # Создание супер-юзера.
            # Create a superuser.
            user = User.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_active=is_active,
                is_superuser=is_superuser
            )

            user.set_password(password)
            user.save()
            print(f'{user.__dict__}\n')
            print('A new superuser has been created!\n')
