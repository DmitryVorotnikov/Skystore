from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_cached_categories():
    '''
    Кеширование списка категории на home-page.
    '''
    if settings.CACHE_ENABLED:
        key = f'category_list'
        subjects = cache.get(key)
        if subjects is None:
            cache_timeout = 60 * 2  # Время жизни кеша, в секундах
            subjects = Category.objects.all()
            cache.set(key, subjects, cache_timeout)
    else:
        subjects = Category.objects.all()
        # self.model.objects.all() = Category.objects.all() - Одинаковые обращения

    return subjects
