from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('creation_date', 'last_modification_date',)

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

        return cleaned_data

    def clean_name(self):
        return self.clean_text('name')

    def clean_description(self):
        return self.clean_text('description')