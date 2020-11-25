from django.forms import ModelForm
from .models import *


class OrderForm(ModelForm):
    class Meta:
        model = Order
        # Vai criar um form na qual todos os campos do model Order está presente, caso fossem somente alguns field seria ['campo1', 'campo2']
        fields = '__all__'


