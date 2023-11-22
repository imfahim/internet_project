from django.urls import path
from internetProject import views
from django.contrib import admin
from django.urls import path, include

app_name = 'internetProject'

urlpatterns = [
    path('', views.index, name='index'),
    path('coin-details/<str:coin_id>/', views.coin_details, name='coin_details'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('currency/<str:from_currency>/<str:to_currency>/', views.currency, name='currency'),
    path('index_jk/', views.index_jk, name='index_jk'),
    path('payment/', views.payment, name='payment'),
]
    