from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login_page/', views.login_page, name='login_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('logout/', views.log_out, name='logout'),
    path('user_page/', views.user_page, name='user_page'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_many_orders/<str:pk>/', views.create_many_orders, name='create_many_orders'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order'),

    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html', ),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

    # Para configurar o gmail para enviar mensagens seguir:
    # https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab
    #Caso seguindo os passos anteriores não funcionarem desativar aqui:
    #https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MVA_IyNi69Hd3GOmh69schMKZSlIwbdlzq9nY4s5bncIUq5HC-vz7C6a2EUlI5YtI1ky2GpWPCxs0dybuALhlqZbFODQ
]
