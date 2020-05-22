from django.forms import ModelForm, TextInput
from .models import ShopCart, Order

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
        widgets = {
            'quantity': TextInput(attrs={
                'class': 'input',
                'type': 'number',
                'value': '1',
            }),
        }

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'surname', 'address', 'city', 'phone']
        widgets = {
            'name': TextInput(attrs={
                'class': 'input',
            }),
            'surname': TextInput(attrs={
                'class': 'input',
            }),
            'address': TextInput(attrs={
                'class': 'input',
            }),
            'city': TextInput(attrs={
                'class': 'input',
            }),
            'phone': TextInput(attrs={
                'class': 'input',
            }),
        }