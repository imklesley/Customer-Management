from django.db import models


class Customer(models.Model):
    # o id é adicionado automágicamente
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    # auto_now_add, adiciona data e horário assim que cria, já auto_now, toda vez que é alterado
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = [('Indoor', 'Indoor'), ('Out door', 'Out door')]

    name = models.CharField(max_length=255, null=True)
    # Para trabalhar com dinheiro, sempre usar DecimalField
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.TextField(help_text='Sua descrição vem aqui', blank=True)
    quantity_available = models.PositiveIntegerField(default=0, )
    date_created = models.DateTimeField(auto_now_add=True)
    # Crio uma relação muitos pra muitos, uma tag pode está em vários produtos e vários produtos podem está numa tag
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = [
        ('Waiting for Payment','Waiting for Payment'),
        ('Preparation', 'Preparation'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    ]


    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=255, choices=STATUS, default=STATUS[0],null=True,)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    note = models.CharField(max_length=1000,null=True)



    def __str__(self):
        return self.product.name
