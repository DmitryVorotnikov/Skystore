from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import Category, Product


class CategoryListView(ListView):
    model = Category


# def home(request):
#     category_list = Category.objects.all()
#
#     context = {
#         'object_list': category_list
#     }
#
#     return render(request, 'catalog/category_list.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}, phone: {phone} message: {message}')
    return render(request, 'catalog/contacts.html')


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
