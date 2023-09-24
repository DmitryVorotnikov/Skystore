from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(default='default_description', verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.PositiveIntegerField(verbose_name='Цена')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_modification_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name}, {self.price}, {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(default='default_description', verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)
