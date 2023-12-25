from django.core.management import call_command
from rest_framework.test import APITestCase

from users.models import User


# todo надо установить рест фреймворк

class CustomCreateSuperUserTestCase(APITestCase):
    """
    Testing a Custom Create SuperUser command.
    """

    def test_create_superuser_successfully(self):
        """ Testing successful user creation. """
        call_command(
            'ccsu',
            '--email=admin@example.com',
            '--password=example_password',
            '--confirm_password=example_password',
            '--first_name=None',
            '--last_name=None',
            '--is_active=test',
            '--is_staff=test',
            '--is_superuser=test'
        )

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertTrue(user_exists)

    def test_exit_email_input(self):
        """ Testing 'exit' during email input. """
        call_command('ccsu', '--email=exit')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)

    def test_invalid_email(self):
        """ Testing invalid email input. """
        call_command('ccsu', '--email=invalid_email')

        user_exists = User.objects.filter(email='invalid_email').exists()
        self.assertFalse(user_exists)

    def test_exit_password_input(self):
        """ Testing 'exit' during password input. """
        call_command('ccsu', '--email=admin@example.com', '--password=exit')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)

    def test_invalid_password(self):
        """ Testing invalid password input. """
        call_command('ccsu', '--email=admin@example.com', '--password=123')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)

    def test_password_mismatch(self):
        """ Testing password mismatch input. """
        call_command('ccsu', '--email=admin@example.com', '--password=example_password',
                     '--confirm_password=mismatch_password')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)
