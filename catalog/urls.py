from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import CategoryListView, ContactsTemplateView, ProductListView, ProductDetailView, ArticleListView, \
    ArticleCreateView, ArticleUpdateView, ArticleDetailView, ArticleDeleteView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', cache_page(60 * 2)(ProductDetailView.as_view()), name='product_item'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    path('articles/', ArticleListView.as_view(), name='articles'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('article/edit/<slug:slug>/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article'),
    path('article/delete/<slug:slug>/', ArticleDeleteView.as_view(), name='article_delete'),
]
