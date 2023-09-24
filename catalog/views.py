from django.shortcuts import render

from catalog.models import Category


def home(request):
    category_list = Category.objects.all()

    context = {
        'object_list': category_list
    }

    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}, phone: {phone} message: {message}')
    return render(request, 'catalog/contacts.html')
