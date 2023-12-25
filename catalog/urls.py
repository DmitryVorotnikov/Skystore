from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import CategoryListView, ContactsTemplateView, ProductListView, ProductDetailView, ArticleListView, \
    ArticleCreateView, ArticleUpdateView, ArticleDetailView, ArticleDeleteView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    # Category
    path('', CategoryListView.as_view(), name='home'),

    # Contacts
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),

    # Products
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', cache_page(60 * 2)(ProductDetailView.as_view()), name='product_item'),
    path('products/create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('products/edit/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_edit'),
    path('products/delete/<int:pk>/', never_cache(ProductDeleteView.as_view()), name='product_delete'),

    # Articles
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('create/', never_cache(ArticleCreateView.as_view()), name='create'),
    path('article/edit/<slug:slug>/', never_cache(ArticleUpdateView.as_view()), name='article_edit'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article'),
    path('article/delete/<slug:slug>/', never_cache(ArticleDeleteView.as_view()), name='article_delete'),
]
