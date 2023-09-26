from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from catalog.models import Category, Product


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


# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'You have new message from {name}, phone: {phone} message: {message}')
#     return render(request, 'catalog/contacts.html')


def products(request):
    product_list = Product.objects.all()

    context = {
        'object_list': product_list
    }

    return render(request, 'catalog/products.html', context)


def product_page(request, pk):
    context = {
        'object': Product.objects.get(pk=pk)
    }

    return render(request, 'catalog/product_page.html', context)
