from django.shortcuts import render, get_object_or_404
from .models import *


def home(request):
    context = {}
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context['orders'] = orders
    context['customers'] = customers
    context['total_orders'] = total_orders
    context['delivered'] = delivered
    context['pending'] = pending

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    context = {}
    all_products = Product.objects.order_by('price')
    context['products'] = all_products

    return render(request, 'accounts/products.html', context)


def customer(request, pk):
    context = {}

    user = get_object_or_404(Customer, pk=pk)
    orders = user.order_set.all()
    context['customer'] = user
    context['orders'] = orders
    return render(request, 'accounts/customer.html', context)
