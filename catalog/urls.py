from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import CategoryListView, ContactsTemplateView, ProductListView, ProductDetailView, ArticleListView, \
    ArticleCreateView, ArticleUpdateView, ArticleDetailView, ArticleDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_item'),

    path('articles/', ArticleListView.as_view(), name='articles'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('article/edit/<slug:slug>/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article'),
    path('article/delete/<slug:slug>/', ArticleDeleteView.as_view(), name='article_delete'),
]