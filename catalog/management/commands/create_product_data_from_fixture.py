import json
from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        fixture_file = 'catalog_product_data.json'

        products_to_create = []
        with open(fixture_file, 'r') as file:
            data = json.load(file)
            for item in data:
                product_fields = item['fields']
                pk = item['pk']
                category_id = product_fields.pop('category')
                category_instance = Category.objects.get(pk=category_id)
                product = Product(pk=pk, category=category_instance, **product_fields)
                products_to_create.append(product)

        Product.objects.bulk_create(products_to_create)
        print('Все объекты из фикстуры добавлены в таблицу Product!')
