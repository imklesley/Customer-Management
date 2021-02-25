from django.shortcuts import render, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages

# Pra adicionar o group de permisão do usuário quando ele está sendo  criado
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
# Verifica se o usuário logou, caso não tenha logado redireciona para a página de login
from django.contrib.auth.decorators import login_required

##
from .filters import OrderFilter
from .forms import *
from .decorators import *


@unauthenticated_user
def register_page(request):
    context = {}
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Ao salvar o formulário, salvo o user criado
            user = form.save()
            # Pego o user name do user, isso para mandar mensagem mais bonitinha para login_page
            username = form.cleaned_data.get('username')



            # Envia a mensagem de sucesso para a próxima page
            messages.success(request, message=f'{username} created with success !')
            return redirect('login_page')

    context['form'] = form
    return render(request, 'accounts/register_page.html', context)


@unauthenticated_user
def login_page(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request=request, message='Your username or password is invalid!')

    return render(request, 'accounts/login_page.html', context)


def log_out(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    context = {}
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    waiting_payment = orders.filter(status='Waiting for Payment').count()
    preparation = orders.filter(status='Preparation').count()
    delivered = orders.filter(status='Delivered').count()

    context['orders'] = orders
    context['total_orders'] = total_orders
    context['waiting_payment'] = waiting_payment
    context['preparation'] = preparation
    context['delivered'] = delivered
    # Só para testesssss
    # Usar %0A  ou %0D para pular linha
    context[
        'whatsapp'] = 'Olá Deusa, Bom dia! Segue Minha Lista de Produtos:%0A*1- Short Jeans tam 34%0A2- Saia Florida Tam 39*'
    return render(request, 'accounts/comum_user.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    context = {}
    customer = request.user.customer
    form = AccountSettingsForm(instance=customer)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, message=f'{request.user.customer.name} Your profile was updated !')
            return redirect('account_settings')

    context['form'] = form

    return render(request=request, template_name='accounts/account_settings.html', context=context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def products(request):
    context = {}
    all_products = Product.objects.order_by('price')
    context['products'] = all_products

    return render(request, 'accounts/products.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    context = {}
    # Procura o usuário em questão
    user = get_object_or_404(Customer, pk=pk)
    # Desse usuário encontrado, pego todos as orders vinculadas ao seu id
    orders = user.order_set.all()

    # Crio um filtro já realizando a pesquisa nas "orders" encontradas anteriormente
    my_filter = OrderFilter(request.GET, orders)
    # Retorno o queryset(qs) dessa pesquisa, caso não encontre retorna para orders []
    # caso encontre mostra os orders encontrados
    orders = my_filter.qs

    context['my_filter'] = my_filter
    context['customer'] = user
    context['orders'] = orders

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def create_many_orders(request, pk):
    context = {}
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5, )
    customerr = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customerr)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customerr)
        if formset.is_valid():
            formset.save()
            return redirect('home')
    context['customer'] = customer
    context['formset'] = formset

    return render(request, 'accounts/many_order_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    context = {}
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context['order'] = order
    return render(request, 'accounts/delete_order.html', context)
