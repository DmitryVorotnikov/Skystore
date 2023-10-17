from getpass import getpass

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    ccsu - custom create super user.
    """
    help = 'Create a superuser with a custom email and password'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        email = options['email'] or input('Enter admin email: ')
        password = options['password'] or getpass('Enter admin password: ')

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
