from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'quantity_available', 'date_created')
    #Para colocar checkboxes no painel admin na parte de tags
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Tag)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'status')


products = Product.objects.filter(name__contains='Je',description__contains='Ouro')

