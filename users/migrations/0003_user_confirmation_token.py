# Generated by Django 4.2.4 on 2023-10-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_need_generate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_token',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Токен подтверждения'),
        ),
    ]