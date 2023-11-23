from django.urls import path
from internetProject import views
from django.contrib import admin
from django.urls import path, include

app_name = 'internetProject'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('currency/<str:from_currency>/<str:to_currency>/', views.currency, name='currency'),
    path('currency_calculate/<str:from_currency>/<str:to_currency>/', views.currency_calculate, name='currency_calculate'),
    path('index_jk/', views.index_jk, name='index_jk'),
    path('payment/', views.payment, name='payment'),
    path('payment_test/<str:from_currency>/<str:to_currency>/', views.payment_test, name='payment_test'),
]
    