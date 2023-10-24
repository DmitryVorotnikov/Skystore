from django import forms

from catalog.models import Product, Version


class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForUserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('creation_date', 'last_modification_date', 'owner_product', 'is_published')

    def clean_text(self, field_name):
        cleaned_data = self.cleaned_data[field_name].lower()

        stoplist = [
            'казино',
            'криптовалюта',
            'крипта',
            'биржа',
            'дешево',
            'бесплатно',
            'обман',
            'полиция',
            'радар'
        ]

        for word in stoplist:
            if word in cleaned_data:
                raise forms.ValidationError(f'{field_name.capitalize()} продукта не допустимо!')
            else:
                cleaned_data = self.cleaned_data[field_name]

        return cleaned_data

    def clean_name(self):
        return self.clean_text('name')

    def clean_description(self):
        return self.clean_text('description')


class ProductForManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('is_published', 'description', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавление чекбокса для is_published
        self.fields['is_published'].widget = forms.CheckboxInput()

    def clean_text(self, field_name):
        cleaned_data = self.cleaned_data[field_name].lower()

        stoplist = [
            'казино',
            'криптовалюта',
            'крипта',
            'биржа',
            'дешево',
            'бесплатно',
            'обман',
            'полиция',
            'радар'
        ]

        for word in stoplist:
            if word in cleaned_data:
                raise forms.ValidationError(f'{field_name.capitalize()} продукта не допустимо!')
            else:
                cleaned_data = self.cleaned_data[field_name]

        return cleaned_data

    def clean_description(self):
        return self.clean_text('description')


class VersionForm(forms.ModelForm):
    version_number = forms.CharField(
        label='Номер версии',
        widget=forms.TextInput(attrs={'placeholder': 'Укажите номер',
                                      'class': 'form-control'})
    )
    name = forms.CharField(
        label='Название версии',
        widget=forms.TextInput(attrs={'placeholder': 'Укажите название',
                                      'class': 'form-control'})
    )
    is_active = forms.BooleanField(
        label='Признак текущей версии',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})

    )

    class Meta:
        model = Version
        fields = '__all__'
