from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import product_page, CategoryListView, ContactsTemplateView, ProductListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', product_page, name='product_page'),
]