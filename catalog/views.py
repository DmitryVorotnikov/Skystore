from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Article, Version


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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(is_published=True)

        return queryset


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published',)
    success_url = reverse_lazy('catalog:articles')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published',)

    def get_success_url(self):
        return reverse('catalog:article', args=[self.kwargs.get('slug')])

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        self.object.number_of_views += 1
        self.object.save()

        return self.object


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('catalog:articles')


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_item', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        print(f'1- {context_data}')

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        print(f'2- {VersionFormset}')
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, self.request.FILES)
            print(f"3- {context_data['formset']}")
            print(f"3,5555- {self.request.POST}")
        else:
            context_data['formset'] = VersionFormset()
            print(f"4- {context_data['formset']}")

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        print(f'5- {formset}')
        self.object = form.save()
        print(f'6- {self.object}')
        print(f'7- {formset.is_valid()}')
        if formset.is_valid():
            formset.instance = self.object
            print(f'8- {formset.instance}')
            formset.save()
            print(f'9 - {formset}')

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:product_item', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')
