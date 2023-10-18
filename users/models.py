from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(_("Email"), unique=True)

    phone_number = models.CharField(_("Phone number"), max_length=35, **NULLABLE)
    country = models.CharField(_("Country"), max_length=100, **NULLABLE)
    avatar = models.ImageField(_("Avatar"), upload_to='users/', **NULLABLE)
    need_generate = models.BooleanField(_("Need generate new password"), default=False)
    confirmation_token = models.CharField(max_length=100, verbose_name='Токен подтверждения', **NULLABLE)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
