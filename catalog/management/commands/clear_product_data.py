from django.core.management import BaseCommand
from catalog.models import Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()
        print('Все объекты в таблице Product удалены!')