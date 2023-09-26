from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import products, product_page, CategoryListView, ContactsTemplateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', products, name='products'),
    path('product/<int:pk>/', product_page, name='product_page'),
]