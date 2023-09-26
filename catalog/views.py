from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView

from catalog.models import Category, Product, Article


class CategoryListView(ListView):
    model = Category


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.method == "POST":
            name = self.request.POST.get('name')
            phone = self.request.POST.get('phone')
            message = self.request.POST.get('message')
            print(f'You have new message from {name}, phone: {phone} message: {message}')

        # Для добавления информации из БД в отображение контактов.
        # context_data['object_list'] = Some_data_for_contacts.objects.all()

        return context_data


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ArticleListView(ListView):
    model = Article
