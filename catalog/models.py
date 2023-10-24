from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(default='default_description', verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.PositiveIntegerField(verbose_name='Цена')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_modification_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    owner_product = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                      verbose_name='Создатель продукта', **NULLABLE)

    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')

    def __str__(self):
        return f'{self.name}, {self.price}, {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)
        # Задаем новые права доступа (ко всей модели и всем полям модели)
        permissions = [
            (
                'set_published',
                'Can change is_published, description, category'
            )
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(default='default_description', verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='Slug', **NULLABLE)
    content = models.TextField(max_length=10000, verbose_name='Содержание')
    preview = models.ImageField(upload_to='article/', verbose_name='Превью', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    number_of_views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('id',)


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт', related_name='versions')
    version_number = models.CharField(max_length=50, verbose_name='Номер версии')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.name} {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('id',)
