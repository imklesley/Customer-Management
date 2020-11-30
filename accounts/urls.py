from django.urls import path
from . import views

urlpatterns = [

    path('login_page/', views.login_page, name='login_page'),
    path('register_page/', views.register_page, name='register_page'),

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_many_orders/<str:pk>/', views.create_many_orders, name='create_many_orders'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),

]
