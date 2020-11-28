from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory

from .models import *
from .forms import *


def home(request):
    context = {}
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    waiting_payment = orders.filter(status='Waiting for Payment').count()
    preparation = orders.filter(status='Preparation').count()

    context['orders'] = orders
    context['customers'] = customers
    context['total_orders'] = total_orders
    context['delivered'] = delivered
    context['waiting_payment'] = waiting_payment
    context['preparation'] = preparation

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


def create_order(request):
    context = {}
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context['form'] = form
    return render(request, 'accounts/order_form.html', context)


def create_many_orders(request, pk):
    context = {}
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5, )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context['customer'] = customer
    context['formset'] = formset

    return render(request, 'accounts/many_order_form.html', context)


def update_order(request, pk):
    context = {}

    # Pego a order de acordo com o id
    order = Order.objects.get(id=pk)

    # para auto preencher os campos basta passar o parametro order
    form = OrderForm(instance=order)

    # verifico se o form é de envío
    if request.method == 'POST':
        # se sim, coloco dentro de form, os campos com os data de order + a informação alterada(caso tenha sido alterda)
        form = OrderForm(request.POST, instance=order)
        # Verifico se está válido
        if form.is_valid():
            form.save()
            # Quando o pagamento tiver sido confirmado, decrementa uma unidade do produto
            if request.POST['status'] == 'Preparation':
                # Pega o id do produto
                product_id = request.POST['product']
                # Busca o produto pelo id
                product = Product.objects.get(pk=product_id)
                # Decrementa uma unidade
                product.quantity_available -= 1
                # Salva a alteração
                product.save()
            return redirect('home')

    context['form'] = form

    return render(request, 'accounts/update_order.html', context)


def delete_order(request, pk):
    context = {}
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context['order'] = order
    return render(request, 'accounts/delete_order.html', context)
