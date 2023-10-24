from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForUserForm, ProductForManagerForm, VersionForm
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

    def get_queryset(self):
        queryset = super().get_queryset()

        # Проверяем, зарегистрирован ли пользователь
        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)

        # Если пользователь является создателем статей (user_product - группа)
        if self.request.user.has_perm('catalog.add_product'):
            current_user = self.request.user
            # Фильтруем продукты по is_published и owner_product
            return queryset.filter(is_published=True, owner_product=current_user)

        # Если пользователь is_staff=True, то отображаем все продукты без исключения.
        if self.request.user.is_staff:
            return queryset

        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ArticleListView(ListView):
    model = Article

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(is_published=True)

        return queryset


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published',)
    success_url = reverse_lazy('catalog:articles')
    permission_required = 'catalog.add_article'

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ('title', 'content', 'preview', 'is_published',)
    permission_required = 'catalog.change_article'

    def get_success_url(self):
        return reverse('catalog:article', args=[self.kwargs.get('slug')])

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()

        return super().form_valid(form)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        self.object.number_of_views += 1
        self.object.save()

        return self.object


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('catalog:articles')
    permission_required = 'catalog.delete_article'


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForUserForm
    permission_required = 'catalog.add_product'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, self.request.FILES)
        else:
            context_data['formset'] = VersionFormset()

        return context_data

    def get_success_url(self):
        return reverse('catalog:product_item', args=[self.object.pk])

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        self.object.owner_product = self.request.user
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.change_product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Если пользователь is_staff можно редактировать
        if self.request.user.is_staff:
            return self.object

        # Вызывает ошибку 404 если текущий пользователь не владелец продукта.
        if self.object.owner_product != self.request.user:
            raise Http404

        return self.object

    def get_form_class(self, *args, **kwargs):
        if self.request.user == self.object.owner_product:
            # Вернуть форму ProductForUserForm для создателя продукта.
            return ProductForUserForm
        elif self.request.user.is_staff and self.request.user.has_perm('catalog.set_published'):
            # Вернуть форму ProductForManagerForm для менеджера.
            return ProductForManagerForm
        else:
            # Вызвать 404 ошибку если ни одно условие не подошло.
            raise Http404

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def get_success_url(self):
        return reverse('catalog:product_item', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        self.object.owner_product = self.request.user
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')
    permission_required = 'catalog.delete_product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        # Вызывает ошибку 404 если текущий пользователь не владелец продукта.
        if self.object.owner_product != self.request.user:
            raise Http404

        return self.object
