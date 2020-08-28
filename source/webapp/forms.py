from django import forms
from django.core.validators import MinValueValidator

from .models import CATEGORY_CHOICES, DEFAULT_CATEGORY, Product, Cart


class DateInput(forms.DateInput):
    input_type = 'date'


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100, required=True, label='Название')
#     description = forms.CharField(max_length=2000, required=False, label='Описание', widget=forms.Textarea)
#     category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True, initial=DEFAULT_CATEGORY,
#                                  label='Категория')
#     amount = forms.IntegerField(min_value=0, required=True, label="Остаток")
#     price = forms.DecimalField(min_value=0, max_digits=7, decimal_places=2, required=True, label='Цена')


class SimpleSeachForm(forms.Form):
    search = forms.CharField(required=False, max_length=100, label='Найти')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'amount', 'price']


class CartForm(forms.Form):
    qty = forms.IntegerField(required=True, initial=1, label='Количество', min_value=0)